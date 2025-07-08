from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Optional, NumberRange

class QuoteForm(FlaskForm):
    # Customer Information
    customer_name = StringField('Customer Name', validators=[DataRequired()])
    customer_address = TextAreaField('Customer Address', validators=[DataRequired()])
    attention_to = StringField('Attention To', validators=[Optional()])

class DoorForm(FlaskForm):
    # Step 1 - Door Configuration
    door_type = SelectField('Door Type', choices=[
        ('', 'Select Door Type'),
        ('Overlap Doors - Swing door', 'Overlap Doors - Swing door'),
        ('Power Operated Sliding door - Single horizontal', 'Power Operated Sliding door - Single horizontal'),
        ('Sliding Door', 'Sliding Door')
    ], validators=[DataRequired()])
    
    cooler_freezer = SelectField('Cooler / Freezer', choices=[
        ('', 'Select Type'),
        ('Cooler', 'Cooler'),
        ('Freezer', 'Freezer')
    ], validators=[DataRequired()])
    
    exterior_type = SelectField('Exterior Type', choices=[
        ('', 'Select Exterior Type'),
        ('Exterior Door - with step sill', 'Exterior Door - with step sill'),
        ('Interior', 'Interior')
    ], validators=[Optional()])
    
    frame_structure = SelectField('Frame Structure', choices=[
        ('', 'Select Frame Structure'),
        ('Aluminium', 'Aluminium'),
        ('Wood', 'Wood')
    ], validators=[DataRequired()])
    
    motorized_manual = SelectField('Motorized/Manual', choices=[
        ('', 'Select Type'),
        ('Manual', 'Manual'),
        ('Motorized', 'Motorized')
    ], validators=[DataRequired()])
    
    width_inches = IntegerField('Width (inches)', validators=[DataRequired(), NumberRange(min=1, max=300)])
    height_inches = IntegerField('Height (inches)', validators=[DataRequired(), NumberRange(min=1, max=300)])
    depth_inches = IntegerField('Depth (inches)', validators=[DataRequired(), NumberRange(min=1, max=20)])
    wall_thickness_inches = IntegerField('Wall Thickness (inches)', validators=[DataRequired(), NumberRange(min=1, max=20)])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1, max=100)], default=1)
    
    # Door Panel and Frame Options
    door_panel = SelectField('Door Panel', choices=[
        ('', 'Select Door Panel'),
        ('26 Ga. White - Stucco Embossed Finish', '26 Ga. White - Stucco Embossed Finish'),
        ('20 Ga. White - Stucco Embossed Finish', '20 Ga. White - Stucco Embossed Finish')
    ], validators=[Optional()])
    
    face_frame = SelectField('Face Frame', choices=[
        ('', 'Select Face Frame'),
        ('Aluminium Frame - Standard', 'Aluminium Frame - Standard'),
        ('Wood Clad. 26 Ga. White - Stucco Embossed', 'Wood Clad. 26 Ga. White - Stucco Embossed')
    ], validators=[Optional()])
    
    inside_jamb = SelectField('Inside Jamb', choices=[
        ('', 'Select Inside Jamb'),
        ('Aluminium Frame - Standard', 'Aluminium Frame - Standard'),
        ('Wood Clad. 26 Ga. White - Stucco Embossed', 'Wood Clad. 26 Ga. White - Stucco Embossed')
    ], validators=[Optional()])
    
    back_frame = SelectField('Back Frame', choices=[
        ('', 'Select Back Frame'),
        ('Aluminium Frame - Standard', 'Aluminium Frame - Standard'),
        ('Wood Clad. 26 Ga. White - Stucco Embossed', 'Wood Clad. 26 Ga. White - Stucco Embossed')
    ], validators=[Optional()])
    
    freezer_door_motor_volts = SelectField('Freezer Door - Motor Volts', choices=[
        ('', 'Select Voltage'),
        ('115VAC/1Phase-60Hz Defrost system', '115VAC/1Phase-60Hz Defrost system'),
        ('230VAC/1Phase-60Hz Defrost system', '230VAC/1Phase-60Hz Defrost system')
    ], validators=[Optional()])
    
    bottom_sweep_weather_strip = SelectField('Bottom Sweep/Weather Strip', choices=[
        ('', 'Select Option'),
        ('Bottom Sweep', 'Bottom Sweep'),
        ('Weather Strip', 'Weather Strip'),
        ('Both', 'Both')
    ], validators=[Optional()])
    
    # Step 2 - Hardware and Additional Options
    interior_release = SelectField('Interior Release', choices=[
        ('', 'Select Option'),
        ('Mushroom Button', 'Mushroom Button'),
        ('Standard Release', 'Standard Release')
    ], validators=[Optional()])
    
    door_closer = SelectField('Door Closer', choices=[
        ('', 'Select Option'),
        ('Spring Door Closer', 'Spring Door Closer'),
        ('Hydraulic Door Closer', 'Hydraulic Door Closer')
    ], validators=[Optional()])
    
    strike = SelectField('Strike', choices=[
        ('', 'Select Option'),
        ('SS6 Strike Chrome 3/4 x 1 5/8', 'SS6 Strike Chrome 3/4 x 1 5/8'),
        ('Standard Strike', 'Standard Strike')
    ], validators=[Optional()])
    
    rain_hood_projection = BooleanField('Rain Hood / Projection', validators=[Optional()])
    wind_chains = BooleanField('Wind Chains', validators=[Optional()])
    internal_light = BooleanField('Internal Light', validators=[Optional()])
    light_switch = BooleanField('Light Switch', validators=[Optional()])
    vent = BooleanField('Vent', validators=[Optional()])
    
    temperature_gauge = SelectField('Temperature Gauge', choices=[
        ('', 'Select Option'),
        ('Standard Temperature Gauge', 'Standard Temperature Gauge'),
        ('Digital Temperature Gauge', 'Digital Temperature Gauge')
    ], validators=[Optional()])
    
    receptacle_box = SelectField('Receptacle Box', choices=[
        ('', 'Select Option'),
        ('Standard Receptacle Box', 'Standard Receptacle Box'),
        ('GFCI Receptacle Box', 'GFCI Receptacle Box')
    ], validators=[Optional()])
    
    junction_box = SelectField('Junction Box', choices=[
        ('', 'Select Option'),
        ('PVC - 4" X 4" X 2"', 'PVC - 4" X 4" X 2"'),
        ('Metal Junction Box', 'Metal Junction Box')
    ], validators=[Optional()])
    
    threshold_plate = SelectField('Threshold Plate', choices=[
        ('', 'Select Option'),
        ('Standard Threshold', 'Standard Threshold'),
        ('Heated Threshold', 'Heated Threshold')
    ], validators=[Optional()])
    
    sliding_door_package = BooleanField('Sliding Door Package', validators=[Optional()])
    
    sliding_door_category = SelectField('Sliding Door Category', choices=[
        ('', 'Select Category'),
        ('Standard', 'Standard'),
        ('Heavy Duty', 'Heavy Duty')
    ], validators=[Optional()])