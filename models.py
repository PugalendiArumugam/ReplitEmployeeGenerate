from app import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, Date

class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_number = Column(String(20), unique=True, nullable=False, index=True)
    employee_name = Column(String(100), nullable=False)
    employee_dob = Column(Date, nullable=False)
    employee_firstname = Column(String(50), nullable=False)
    employee_lastname = Column(String(50), nullable=False)
    employee_city = Column(String(50), nullable=False)
    created_at = Column(db.DateTime, default=datetime.utcnow)
    updated_at = Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Employee {self.employee_number}: {self.employee_name}>'
    
    def to_dict(self):
        """Convert employee object to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'employee_number': self.employee_number,
            'employee_name': self.employee_name,
            'employee_dob': self.employee_dob.isoformat() if self.employee_dob else None,
            'employee_firstname': self.employee_firstname,
            'employee_lastname': self.employee_lastname,
            'employee_city': self.employee_city,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
