from marshmallow import Schema, fields, ValidationError, validates
from datetime import datetime
import re

class EmployeeSchema(Schema):
    id = fields.Int(dump_only=True)
    employee_number = fields.Str(required=True, validate=lambda x: len(x.strip()) > 0)
    employee_name = fields.Str(required=True, validate=lambda x: len(x.strip()) > 0)
    employee_dob = fields.Date(required=True)
    employee_firstname = fields.Str(required=True, validate=lambda x: len(x.strip()) > 0)
    employee_lastname = fields.Str(required=True, validate=lambda x: len(x.strip()) > 0)
    employee_city = fields.Str(required=True, validate=lambda x: len(x.strip()) > 0)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    @validates('employee_number')
    def validate_employee_number(self, value):
        """Validate employee number format"""
        if not value or not value.strip():
            raise ValidationError('Employee number cannot be empty')
        
        # Check if employee number contains only alphanumeric characters and hyphens
        if not re.match(r'^[A-Za-z0-9\-]+$', value.strip()):
            raise ValidationError('Employee number can only contain letters, numbers, and hyphens')
    
    @validates('employee_firstname')
    def validate_firstname(self, value):
        """Validate first name"""
        if not value or not value.strip():
            raise ValidationError('First name cannot be empty')
        
        if len(value.strip()) < 2:
            raise ValidationError('First name must be at least 2 characters long')
    
    @validates('employee_lastname')
    def validate_lastname(self, value):
        """Validate last name"""
        if not value or not value.strip():
            raise ValidationError('Last name cannot be empty')
        
        if len(value.strip()) < 2:
            raise ValidationError('Last name must be at least 2 characters long')
    
    @validates('employee_dob')
    def validate_dob(self, value):
        """Validate date of birth"""
        if not value:
            raise ValidationError('Date of birth is required')
        
        # Check if date is not in the future
        if value > datetime.now().date():
            raise ValidationError('Date of birth cannot be in the future')
        
        # Check if age is reasonable (between 16 and 100 years)
        age = (datetime.now().date() - value).days / 365.25
        if age < 16:
            raise ValidationError('Employee must be at least 16 years old')
        if age > 100:
            raise ValidationError('Employee age cannot exceed 100 years')

# Create schema instances
employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)
