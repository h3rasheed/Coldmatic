import re
from flask import render_template, request, redirect, url_for, flash, make_response, jsonify
from app import app, db
from models import Quote, Door
from forms import QuoteForm, DoorForm
from pricing_calculator import PricingCalculator
from pdf_generator import QuotePDFGenerator
from datetime import datetime

@app.route('/')
def index():
    """Main quote form page"""
    quote_form = QuoteForm()
    door_form = DoorForm()
    return render_template('new_door_quote.html', quote_form=quote_form, door_form=door_form)

def generate_quote_number():
    """Generate a unique quote number based on date and sequence."""
    today = datetime.now().strftime('%Y%m%d')
    last_quote = db.session.query(Quote).filter(Quote.quote_number.like(f'{today}%')).order_by(Quote.id.desc()).first()
    sequence = int(last_quote.quote_number[-4:]) + 1 if last_quote else 1
    return f'{today}{sequence:04d}'

@app.route('/generate_quote', methods=['POST'])
def generate_quote():
    # Initialize PricingCalculator
    calculator = PricingCalculator()

    # Parse form data
    form_data = request.form
    customer_data = {
        'customer_name': form_data.get('customer_name', ''),
        'customer_address': form_data.get('customer_address', ''),
        'attention_to': form_data.get('attention_to', '')
    }

    # Validate customer data
    if not customer_data['customer_name'] or not customer_data['customer_address']:
        flash('Customer Name and Address are required', 'error')
        return render_template('new_door_quote.html', quote_form=QuoteForm(), door_form=DoorForm())

    # Parse doors data
    doors_data = {}
    for key, value in form_data.items():
        match = re.match(r'doors\[(\d+)\]\[(.+)\]', key)
        if match:
            door_id, field = match.groups()
            if door_id not in doors_data:
                doors_data[door_id] = {}
            # Convert numeric fields to integers
            if field in ['quantity','markup_percentage', 'width_inches', 'height_inches', 'depth_inches', 'wall_thickness_inches']:
                doors_data[door_id][field] = int(value) if value else 0
            # Convert checkbox fields to boolean
            elif field in ['rain_hood_projection', 'wind_chains', 'internal_light', 'light_switch', 'vent', 'sliding_door_package']:
                doors_data[door_id][field] = value == 'y'
            else:
                doors_data[door_id][field] = value

    # Validate doors data
    required_fields = ['door_type', 'cooler_freezer', 'frame_structure', 'motorized_manual', 
                       'quantity', 'width_inches', 'height_inches', 'depth_inches', 'wall_thickness_inches']
    errors = []
    for door_id, door_data in doors_data.items():
        door_errors = {}
        for field in required_fields:
            if not door_data.get(field):
                door_errors[field] = f'{field.replace("_", " ").title()} is required'
        if door_errors:
            errors.append({'door_id': door_id, 'errors': door_errors})

    if errors:
        flash('Please fill in all required door fields', 'error')
        return render_template('new_door_quote.html', quote_form=QuoteForm(), door_form=DoorForm(), errors={'doors': errors})

    # Create Quote instance
    quote = Quote(
        quote_number=generate_quote_number(),
        created_date=datetime.now(),
        customer_name=customer_data['customer_name'],
        attention_to=customer_data['attention_to'],
        customer_address=customer_data['customer_address'],
        base_price=0.0,
        options_price=0.0,
        labor_expense=0.0,
        material_expense=0.0,
        total_price=0.0,
        status='draft'
    )
    db.session.add(quote)
    db.session.flush()

    total_base_price = 0.0
    total_material_expense = 0.0
    total_options_price = 0.0
    total_labor_expense = 0.0
    total_price = 0.0
    processed_doors = []

    for door_id, door_data in doors_data.items():
        # Calculate pricing
        pricing = calculator.calculate_total_quote(door_data)
        door = Door(
            quote_id=quote.id,
            door_type=door_data.get('door_type', ''),
            cooler_freezer=door_data.get('cooler_freezer', ''),
            frame_structure=door_data.get('frame_structure', ''),
            motorized_manual=door_data.get('motorized_manual', ''),
            exterior_type=door_data.get('exterior_type', ''),
            quantity=door_data.get('quantity', 1),
            markup_percentage=door_data.get('markup_percentage', 30),
            width_inches=door_data.get('width_inches', 0),
            height_inches=door_data.get('height_inches', 0),
            depth_inches=door_data.get('depth_inches', 0),
            wall_thickness_inches=door_data.get('wall_thickness_inches', 0),
            door_panel=door_data.get('door_panel', ''),
            face_frame=door_data.get('face_frame', ''),
            inside_jamb=door_data.get('inside_jamb', ''),
            back_frame=door_data.get('back_frame', ''),
            freezer_door_motor_volts=door_data.get('freezer_door_motor_volts', ''),
            bottom_sweep_weather_strip=door_data.get('bottom_sweep_weather_strip', ''),
            interior_release=door_data.get('interior_release', ''),
            door_closer=door_data.get('door_closer', ''),
            strike=door_data.get('strike', ''),
            rain_hood_projection=door_data.get('rain_hood_projection', False),
            wind_chains=door_data.get('wind_chains', False),
            internal_light=door_data.get('internal_light', False),
            light_switch=door_data.get('light_switch', False),
            vent=door_data.get('vent', False),
            sliding_door_package=door_data.get('sliding_door_package', False),
            temperature_gauge=door_data.get('temperature_gauge', ''),
            receptacle_box=door_data.get('receptacle_box', ''),
            junction_box=door_data.get('junction_box', ''),
            threshold_plate=door_data.get('threshold_plate', ''),
            sliding_door_category=door_data.get('sliding_door_category', ''),
            base_price=pricing['base_price'],
            material_expense=pricing['material_cost'],
            options_price=pricing['hardware_cost'],
            labor_expense=pricing['labor_cost'],
            total_price=pricing['total_price']
        )
        db.session.add(door)
        total_base_price += pricing['base_price']
        total_material_expense += pricing['material_cost']
        total_options_price += pricing['hardware_cost']
        total_labor_expense += pricing['labor_cost']
        total_price += pricing['total_price']
        processed_doors.append(door_data)

    # Update Quote with aggregated pricing
    quote.base_price = total_base_price
    quote.material_expense = total_material_expense
    quote.options_price = total_options_price
    quote.labor_expense = total_labor_expense
    quote.total_price = total_price
    db.session.commit()

    # Generate PDF (uncomment when PDF generator is ready)
    # pdf_path = QuotePDFGenerator.generate_quote_pdf(quote, processed_doors)
    return redirect(url_for('view_quote', quote_id=quote.id))

@app.route('/quote/<int:quote_id>')
def view_quote(quote_id):
    """View a specific quote"""
    quote = Quote.query.get_or_404(quote_id)
    return render_template('quote_view.html', quote=quote)
from flask import make_response, redirect, url_for, flash
from app import app, db
from models import Quote
from pdf_generator import QuotePDFGenerator

@app.route('/quote/<int:quote_id>/pdf')
def download_quote_pdf(quote_id):
    """Download quote as PDF"""
    quote = Quote.query.get_or_404(quote_id)
    
    try:
        # Prepare quote data
        quote_data = {
            'quote_number': quote.quote_number,
            'customer_name': quote.customer_name,
            'customer_address': quote.customer_address,
            'attention_to': quote.attention_to,
            'created_date': quote.created_date.strftime('%B %d, %Y'),
            'status': quote.status,
            'doors': [
                {
                    'door_type': door.door_type,
                    'cooler_freezer': door.cooler_freezer,
                    'width_inches': door.width_inches,
                    'height_inches': door.height_inches,
                    'depth_inches': door.depth_inches,
                    'quantity': door.quantity,
                    'markup_percentage': door.markup_percentage,
                    'door_panel': door.door_panel,
                    'face_frame': door.face_frame,
                    'frame_structure': door.frame_structure,
                    'motorized_manual': door.motorized_manual,
                    'exterior_type': door.exterior_type,
                    'inside_jamb': door.inside_jamb,
                    'back_frame': door.back_frame,
                    'freezer_door_motor_volts': door.freezer_door_motor_volts,
                    'bottom_sweep_weather_strip': door.bottom_sweep_weather_strip,
                    'interior_release': door.interior_release,
                    'door_closer': door.door_closer,
                    'strike': door.strike,
                    'threshold_plate': door.threshold_plate,
                    'rain_hood_projection': door.rain_hood_projection,
                    'wind_chains': door.wind_chains,
                    'internal_light': door.internal_light,
                    'light_switch': door.light_switch,
                    'vent': door.vent,
                    'sliding_door_package': door.sliding_door_package,
                    'temperature_gauge': door.temperature_gauge,
                    'receptacle_box': door.receptacle_box,
                    'junction_box': door.junction_box,
                    'sliding_door_category': door.sliding_door_category,
                    'base_price': float(door.base_price or 0),
                    'material_expense': float(door.material_expense or 0),
                    'options_price': float(door.options_price or 0),
                    'labor_expense': float(door.labor_expense or 0),
                    'total_price': float(door.total_price or 0)
                } for door in quote.doors
            ]
        }
        
        pricing_data = {
            'base_price': float(quote.base_price or 0),
            'material_expense': float(quote.material_expense or 0),
            'options_price': float(quote.options_price or 0),
            'labor_expense': float(quote.labor_expense or 0),
            'total_price': float(quote.total_price or 0)
        }
        
        # Generate PDF
        pdf_generator = QuotePDFGenerator()
        pdf_buffer = pdf_generator.generate_quote_pdf(quote_data, pricing_data)
        
        # Create response
        response = make_response(pdf_buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=Quote_{quote.quote_number}.pdf'
        
        return response
        
    except Exception as e:
        app.logger.error(f"PDF generation error: {str(e)}")
        flash('Error generating PDF. Please try again.', 'error')
        return redirect(url_for('view_quote', quote_id=quote_id))
    

@app.route('/quotes')
def list_quotes():
    """List all quotes"""
    quotes = Quote.query.order_by(Quote.created_date.desc()).all()
    return render_template('quotes_list.html', quotes=quotes)


from flask import flash, redirect, url_for
from app import app, db
from models import Quote

@app.route('/quote/<int:quote_id>/delete', methods=['POST'])
def delete_quote(quote_id):
    """Delete a quote and its associated doors"""
    quote = Quote.query.get_or_404(quote_id)
    try:
        db.session.delete(quote)
        db.session.commit()
        flash(f"Quote #{quote.quote_number} deleted successfully", "success")
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error deleting quote {quote_id}: {str(e)}")
        flash("Error deleting quote. Please try again.", "error")
    return redirect(url_for('list_quotes'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500