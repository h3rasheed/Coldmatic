from app import db
from datetime import datetime
from sqlalchemy import Text, Numeric, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class Quote(db.Model):
    id = db.Column(Integer, primary_key=True)
    quote_number = db.Column(String(50), unique=True, nullable=False)
    created_date = db.Column(DateTime, default=datetime.utcnow)
    
    # Customer Information
    customer_name = db.Column(String(200))
    customer_address = db.Column(Text)
    attention_to = db.Column(String(200))
    
    # Pricing
    base_price = db.Column(Numeric(10, 2), default=0.00)
    options_price = db.Column(Numeric(10, 2), default=0.00)
    labor_expense = db.Column(Numeric(10, 2), default=0.00)
    material_expense = db.Column(Numeric(10, 2), default=0.00)
    total_price = db.Column(Numeric(10, 2), default=0.00)
    
    # Relationship to Doors
    doors = relationship('Door', back_populates='quote', cascade='all, delete-orphan')
    
    # Status
    status = db.Column(String(20), default='draft')  # draft, sent, approved, etc.

class Door(db.Model):
    id = db.Column(Integer, primary_key=True)
    quote_id = db.Column(Integer, ForeignKey('quote.id', ondelete='CASCADE'), nullable=False)
    quote = relationship('Quote', back_populates='doors')
    
    # Door Configuration - Step 1
    door_type = db.Column(String(100))
    cooler_freezer = db.Column(String(50))
    exterior_type = db.Column(String(100))
    frame_structure = db.Column(String(50))
    motorized_manual = db.Column(String(20))
    width_inches = db.Column(Integer)
    height_inches = db.Column(Integer)
    depth_inches = db.Column(Integer)
    markup_percentage = db.Column(Integer)
    wall_thickness_inches = db.Column(Integer)
    quantity = db.Column(Integer, default=1)
    
    # Door Panel and Frame Options
    door_panel = db.Column(String(200))
    face_frame = db.Column(String(200))
    inside_jamb = db.Column(String(200))
    back_frame = db.Column(String(200))
    freezer_door_motor_volts = db.Column(String(50))
    bottom_sweep_weather_strip = db.Column(String(200))
    
    # Step 2 - Additional Options
    interior_release = db.Column(String(100))
    door_closer = db.Column(String(100))
    strike = db.Column(String(100))
    rain_hood_projection = db.Column(Boolean, default=False)
    wind_chains = db.Column(Boolean, default=False)
    internal_light = db.Column(Boolean, default=False)
    light_switch = db.Column(Boolean, default=False)
    vent = db.Column(Boolean, default=False)
    temperature_gauge = db.Column(String(100))
    receptacle_box = db.Column(String(100))
    junction_box = db.Column(String(100))
    threshold_plate = db.Column(String(100))
    sliding_door_package = db.Column(Boolean, default=False)
    sliding_door_category = db.Column(String(100))
    
    # Pricing
    base_price = db.Column(Numeric(10, 2), default=0.00)
    options_price = db.Column(Numeric(10, 2), default=0.00)
    labor_expense = db.Column(Numeric(10, 2), default=0.00)
    material_expense = db.Column(Numeric(10, 2), default=0.00)
    total_price = db.Column(Numeric(10, 2), default=0.00)