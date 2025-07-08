from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from datetime import datetime
from io import BytesIO

class QuotePDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CompanyHeader',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=0,
            textColor=colors.black,
            alignment=TA_LEFT
        ))
        
        self.styles.add(ParagraphStyle(
            name='CompanyInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=0,
            textColor=colors.black,
            alignment=TA_LEFT
        ))
        
        self.styles.add(ParagraphStyle(
            name='QuoteHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.black,
            alignment=TA_LEFT
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading3'],
            fontSize=12,
            spaceBefore=10,
            spaceAfter=6,
            textColor=colors.black,
            alignment=TA_LEFT
        ))
        
        self.styles.add(ParagraphStyle(
            name='NormalSmall',
            parent=self.styles['Normal'],
            fontSize=10,
            leading=12,
            spaceAfter=4
        ))
    
    def generate_quote_pdf(self, quote_data, pricing_data):
        """Generate a complete quote PDF"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=0.5*inch, leftMargin=0.5*inch,
                              topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        # Build the document content
        story = []
        
        # Company header with logo
        story.extend(self._build_company_header())
        story.append(Spacer(1, 0.25*inch))
        
        # Quote information
        story.extend(self._build_quote_info(quote_data))
        story.append(Spacer(1, 0.2*inch))
        
        # Customer information
        story.extend(self._build_customer_info(quote_data))
        story.append(Spacer(1, 0.2*inch))
        
        # Door specifications
        story.extend(self._build_door_specifications(quote_data))
        story.append(Spacer(1, 0.2*inch))
        
        # Pricing breakdown
        story.extend(self._build_pricing_breakdown(pricing_data))
        story.append(Spacer(1, 0.2*inch))
        
        # Terms and conditions
        story.extend(self._build_terms_and_conditions())
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def _build_company_header(self):
        """Build company header section with 50% company details and 50% logo"""
        elements = []
        
        # Company details
        company_info = [
            ["Coldmatic Building Systems Inc.", ""],
            ["61 Baywood Rd.", ""],
            ["Toronto, ON, M9V 3Y8", ""],
            ["Tel: 416 744 7600", ""],
            ["www.coldmatic.com", ""]
        ]
        
        # Logo (adjust path to your actual logo file)
        logo_path = "static/images/logo.jpg"  # Ensure this path is correct
        logo = Image(logo_path, width=3*inch, height=1*inch)  # Adjust size as needed
        
        # Header table: 50% company details, 50% logo
        header_data = [[Table(company_info, colWidths=[2.5*inch]), logo]]
        header_table = Table(header_data, colWidths=[3.5*inch, 3.5*inch])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ]))
        elements.append(header_table)
        
        return elements
    
    def _build_quote_info(self, quote_data):
        """Build quote information section"""
        elements = []
        
        # Create a table for date and quote number
        quote_date = quote_data.get('created_date', datetime.now().strftime("%B %d, %Y"))
        quote_number = quote_data.get('quote_number', 'DRAFT')
        
        data = [
            [f"Date: {quote_date}", f"Quote #: {quote_number}"]
        ]
        table = Table(data, colWidths=[3.5*inch, 3.5*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ]))
        elements.append(table)
        
        return elements
    
    def _build_customer_info(self, quote_data):
        """Build customer information section"""
        elements = []
        
        elements.append(Paragraph("Customer Information", self.styles['SectionHeader']))
        
        customer_name = quote_data.get('customer_name', '').upper()
        attention_to = quote_data.get('attention_to', '')
        customer_address = quote_data.get('customer_address', '')
        
        elements.append(Paragraph(f"<b>{customer_name}</b>", self.styles['NormalSmall']))
        if attention_to:
            elements.append(Paragraph(f"Sales Rep: {attention_to}", self.styles['NormalSmall']))
        if customer_address:
            elements.append(Paragraph(customer_address, self.styles['NormalSmall']))
        
        elements.append(Paragraph("<b>Proposal for Supply of Door</b>", self.styles['SectionHeader']))
        
        return elements
    
    def _build_door_specifications(self, quote_data):
        """Build door specifications section for multiple doors"""
        elements = []
        
        elements.append(Paragraph("Door Specifications", self.styles['SectionHeader']))
        
        for i, door in enumerate(quote_data.get('doors', []), 1):
            elements.append(Paragraph(f"Door {i}:", self.styles['SectionHeader']))
            
            # Door Type and Dimensions
            dimensions = f"{door['width_inches']}\" x {door['height_inches']}\" {door['depth_inches']}\" Thick"
            door_description = f"{door['cooler_freezer']} {door['door_type']}: {dimensions}"
            elements.append(Paragraph(door_description, self.styles['NormalSmall']))
            
            # Finish
            finish = door['exterior_type'] or door['door_panel'] or 'N/A'
            elements.append(Paragraph(f"Finish: {finish}", self.styles['NormalSmall']))
            
            # Frame
            frame = f"{door['frame_structure'] or 'Standard'}"
            frame_parts = [part for part in [door['face_frame'], door['inside_jamb'], door['back_frame']] if part]
            if frame_parts:
                frame += f" - {', '.join(frame_parts)}"
            elements.append(Paragraph(f"Frame: {frame}", self.styles['NormalSmall']))
            
            # Hardware
            hardware = [item for item in [door['interior_release'], door['door_closer'], door['strike']] if item]
            hardware_text = ", ".join(hardware) if hardware else "None"
            elements.append(Paragraph(f"Hardware: {hardware_text}", self.styles['NormalSmall']))
            
            # Threshold Plate
            threshold = door['threshold_plate'] or 'None'
            elements.append(Paragraph(f"Threshold Plate: {threshold}", self.styles['NormalSmall']))
            
            # Temperature
            temp = "35°F / 2°C" if door['cooler_freezer'] == "Cooler" else "0°F / -18°C" if door['cooler_freezer'] == "Freezer" else "N/A"
            elements.append(Paragraph(f"{door['cooler_freezer']} Good for Temperature: {temp}", self.styles['NormalSmall']))
            
            # Additional Options
            options = []
            if door['rain_hood_projection']:
                options.append("Rain Hood / Projection")
            if door['wind_chains']:
                options.append("Wind Chains")
            if door['internal_light']:
                options.append("Internal Light")
            if door['light_switch']:
                options.append("Light Switch")
            if door['vent']:
                options.append("Vent")
            if door['sliding_door_package']:
                options.append("Sliding Door Package")
            if options:
                elements.append(Paragraph(f"Additional Options: {', '.join(options)}", self.styles['NormalSmall']))
            
            # Pricing
            elements.append(Paragraph(f"Pricing Doors - ${door['total_price']:.2f}", self.styles['NormalSmall']))
            elements.append(Spacer(1, 0.1*inch))
        
        return elements
    
    def _build_pricing_breakdown(self, pricing_data):
        """Build pricing breakdown section"""
        elements = []
        
        elements.append(Paragraph("Pricing Breakdown", self.styles['SectionHeader']))
        
        data = [
            ["Base Price:", f"${pricing_data['base_price']:.2f}"],
            ["Material Expense:", f"${pricing_data['material_expense']:.2f}"],
            ["Options Price:", f"${pricing_data['options_price']:.2f}"],
            ["Labor Expense:", f"${pricing_data['labor_expense']:.2f}"],
            ["Total Price:", f"${pricing_data['total_price']:.2f} CAD + Applicable taxes"]
        ]
        
        table = Table(data, colWidths=[2*inch, 4.5*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4)
        ]))
        elements.append(table)
        
        return elements
    
    def _build_terms_and_conditions(self):
        """Build terms and conditions section"""
        elements = []
        
        elements.append(Paragraph("Lead Times & Expedite Fees", self.styles['SectionHeader']))
        elements.append(Paragraph("Standard Lead Time: 4-6 weeks from the receipt of approved drawings.", 
                                self.styles['NormalSmall']))
        elements.append(Paragraph("Expedited Lead Time: (2)-week rush service available at an additional fee of 30%, subject to approval based on production schedule adjustments.", 
                                self.styles['NormalSmall']))
        
        elements.append(Spacer(1, 0.15*inch))
        elements.append(Paragraph("Important Notes:", self.styles['SectionHeader']))
        
        notes = [
            "• Pricing is plus applicable taxes in Canadian Funds. Pricing is good for Net 15 Days Only.",
            "• Pricing is for supply only and is based on the provided drawings and specifications.",
            "• FOB our Plant in Etobicoke. Order is Crated.",
            "• Complimentary drawing revisions are included for up to three versions. Any additional revisions will incur a fee of $95.00 + tax per version.",
            "• Orders canceled during the drawing phase will be subject to an administrative and CAD fee of $200.00 + tax."
        ]
        
        for note in notes:
            elements.append(Paragraph(note, self.styles['NormalSmall']))
        
        elements.append(Spacer(1, 0.1*inch))
        elements.append(Paragraph("Please note that all prices are subject to change without notice. In the event that new tariffs are levied against Canada, we reserve the right to adjust our pricing accordingly to reflect any increased costs. We will make reasonable efforts to notify our customers of any such price changes in a timely manner.", 
                                self.styles['NormalSmall']))
        
        elements.append(Spacer(1, 0.15*inch))
        elements.append(Paragraph("Terms: Net 30 days from date of Invoice submitted. Price offered is valid for 15 Days from offered date in Canadian Dollars.", 
                                self.styles['NormalSmall']))
        
        return elements