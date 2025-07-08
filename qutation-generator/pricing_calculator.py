"""
Pricing calculator that mimics the Excel formulas for door quotations
"""

class PricingCalculator:
    def __init__(self):
        # Base prices matching Excel structure - Door 1 Min. Cost Price
        self.base_prices = {
            'Overlap Doors - Swing door': {
                'Cooler': {
                    'base': 1150.68,  # From Excel screenshots
                    'markup': 0.30    # 30% markup as shown
                },
                'Freezer': {
                    'base': 1495.88,  # Step up pricing for freezer
                    'markup': 0.30
                }
            },
            'Power Operated Sliding door - Single horizontal': {
                'Cooler': {
                    'base': 8187.27,
                    'markup': 0.30
                },
                'Freezer': {
                    'base': 8187.27,
                    'markup': 0.30
                }
            },
            'Sliding Door': {
                'Cooler': {
                    'base': 1800.00,
                    'markup': 0.30
                },
                'Freezer': {
                    'base': 2100.00,
                    'markup': 0.30
                }
            }
        }
        
        # Hardware and options pricing - matching Excel Additional Options prices
        self.hardware_prices = {
            # Interior Release options
            'Mushroom Button': 13.93,
            'Standard Release': 10.00,
            
            # Door Closer options
            'Spring Door Closer': 41.33,
            'Hydraulic Door Closer': 65.00,
            
            # Strike options
            'SS6 Strike Chrome 3/4 x 1 5/8': 45.82,
            'Standard Strike': 35.00,
            
            # Additional options (checkboxes)
            'rain_hood_projection': 50.00,
            'wind_chains': 25.00,
            'internal_light': 75.00,
            'light_switch': 15.00,
            'vent': 35.00,
            
            # Technical equipment
            'Standard Temperature Gauge': 85.00,
            'Digital Temperature Gauge': 125.00,
            'Standard Receptacle Box': 45.00,
            'GFCI Receptacle Box': 65.00,
            'PVC - 4" X 4" X 2"': 25.00,
            'Metal Junction Box': 35.00,
            'Standard Threshold': 50.00,
            'Heated Threshold': 150.00
        }
        
        # Material costs
        self.material_costs = {
            'door_panel': {
                '26 Ga. White - Stucco Embossed Finish': 93.60,
                '20 Ga. White - Stucco Embossed Finish': 125.00
            },
            'face_frame': {
                'Aluminium Frame - Standard': 246.35,
                'Wood Clad. 26 Ga. White - Stucco Embossed': 285.00
            },
            'inside_jamb': {
                'Aluminium Frame - Standard': 55.50,
                'Wood Clad. 26 Ga. White - Stucco Embossed': 75.00
            },
            'back_frame': {
                'Aluminium Frame - Standard': 72.39,
                'Wood Clad. 26 Ga. White - Stucco Embossed': 95.00
            },
            'freezer_door_motor_volts': {
                '115VAC/1Phase-60Hz Defrost system': 180.00,
                '230VAC/1Phase-60Hz Defrost system': 200.00
            },
            'bottom_sweep_weather_strip': {
                'Bottom Sweep': 19.30,
                'Weather Strip': 25.00,
                'Both': 40.31
            }
        }
        
        # Labor costs
        self.labor_costs = {
            'labor_expense': 281.67,
            'foam_expense': 43.64
        }
        
        # Sliding door parts pricing
        self.sliding_door_prices = {
            'Standard': 0.00,
            'Heavy Duty': 150.00
        }
    
    def calculate_base_price(self, door_type, cooler_freezer, width, height, depth, quantity=1):
        """Calculate base door price based on type and dimensions"""
        if door_type not in self.base_prices or cooler_freezer not in self.base_prices[door_type]:
            return 0.00
        
        config = self.base_prices[door_type][cooler_freezer]
        base_price = config['base']
        
        # Size adjustments (simplified - in real Excel this would be more complex)
        standard_width = 34
        standard_height = 65
        
        if width > standard_width:
            width_premium = (width - standard_width) * 15.00
            base_price += width_premium
        
        if height > standard_height:
            height_premium = (height - standard_height) * 12.00
            base_price += height_premium
        
        # Depth premium for thicker doors
        if depth > 4:
            depth_premium = (depth - 4) * 50.00
            base_price += depth_premium
        
        # Apply markup
        base_price_with_markup = base_price * (1 + config['markup'])
        
        return round(base_price_with_markup * quantity, 2)
    
    def calculate_material_costs(self, form_data):
        """Calculate material costs based on selected options"""
        total_material_cost = 0.00
        
        # Door panel cost
        if form_data.get('door_panel'):
            total_material_cost += self.material_costs['door_panel'].get(form_data['door_panel'], 0)
        
        # Frame costs
        if form_data.get('face_frame'):
            total_material_cost += self.material_costs['face_frame'].get(form_data['face_frame'], 0)
        
        if form_data.get('inside_jamb'):
            total_material_cost += self.material_costs['inside_jamb'].get(form_data['inside_jamb'], 0)
        
        if form_data.get('back_frame'):
            total_material_cost += self.material_costs['back_frame'].get(form_data['back_frame'], 0)
        
        # Motor volts for freezer doors
        if form_data.get('freezer_door_motor_volts'):
            total_material_cost += self.material_costs['freezer_door_motor_volts'].get(form_data['freezer_door_motor_volts'], 0)
        
        # Bottom sweep/weather strip
        if form_data.get('bottom_sweep_weather_strip'):
            total_material_cost += self.material_costs['bottom_sweep_weather_strip'].get(form_data['bottom_sweep_weather_strip'], 0)
        
        return round(total_material_cost, 2)
    
    def calculate_hardware_costs(self, form_data):
        """Calculate hardware and additional options costs"""
        total_hardware_cost = 0.00
        
        # Hardware selections
        hardware_fields = ['interior_release', 'door_closer', 'strike', 'temperature_gauge', 
                          'receptacle_box', 'junction_box', 'threshold_plate']
        
        for field in hardware_fields:
            if form_data.get(field):
                total_hardware_cost += self.hardware_prices.get(form_data[field], 0)
        
        # Boolean options
        boolean_options = ['rain_hood_projection', 'wind_chains', 'internal_light', 
                          'light_switch', 'vent']
        
        for option in boolean_options:
            if form_data.get(option):
                total_hardware_cost += self.hardware_prices.get(option, 0)
        
        # Sliding door package
        if form_data.get('sliding_door_package') and form_data.get('sliding_door_category'):
            total_hardware_cost += self.sliding_door_prices.get(form_data['sliding_door_category'], 0)
        
        return round(total_hardware_cost, 2)
    
    def calculate_labor_costs(self, form_data):
        """Calculate labor costs"""
        quantity = form_data.get('quantity', 1)
        base_labor = self.labor_costs['labor_expense']
        foam_cost = self.labor_costs['foam_expense']
        
        total_labor = (base_labor + foam_cost) * quantity
        return round(total_labor, 2)
    
    def calculate_total_quote(self, form_data):
        """Calculate the complete quote with all components"""
        door_type = form_data.get('door_type', '')
        cooler_freezer = form_data.get('cooler_freezer', '')
        width = form_data.get('width_inches', 34)
        height = form_data.get('height_inches', 65)
        depth = form_data.get('depth_inches', 4)
        quantity = form_data.get('quantity', 1)
        
        # Calculate all components
        base_price = self.calculate_base_price(door_type, cooler_freezer, width, height, depth, quantity)
        material_cost = self.calculate_material_costs(form_data)
        hardware_cost = self.calculate_hardware_costs(form_data)
        labor_cost = self.calculate_labor_costs(form_data)
        
        # Total before markup
        subtotal = base_price + material_cost + hardware_cost + labor_cost
        
        # Final total (no additional markup on subtotal)
        total_price = subtotal
        
        return {
            'base_price': base_price,
            'material_cost': material_cost,
            'hardware_cost': hardware_cost,
            'labor_cost': labor_cost,
            'subtotal': subtotal,
            'total_price': round(total_price, 2)
        }
