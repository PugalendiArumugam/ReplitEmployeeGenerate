from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app import db
from models import Employee
from serializers import employee_schema, employees_schema
import logging

# Create blueprint for API routes
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

@api_bp.route('/employees', methods=['POST'])
def create_employee():
    """Create a new employee"""
    print("Post request to add an employees")
    try:
        # Get JSON data from request
        json_data = request.get_json()

        if not json_data:
            return jsonify({'error': 'No input data provided'}), 400
        
        # Validate and deserialize input
        try:
            employee_data = employee_schema.load(json_data)

        except ValidationError as err:
            return jsonify({'error': 'Validation error', 'messages': err.messages}), 400
        
        # Check if employee number already exists
        existing_employee = Employee.query.filter_by(employee_number=employee_data['employee_number']).first()


        if existing_employee:
            return jsonify({'error': 'Employee number already exists'}), 409
        
        # Create new employee
        employee = Employee(**employee_data)
        db.session.add(employee)
        db.session.commit()
        
        logging.info(f"Created employee: {employee.employee_number}")
        
        # Return created employee
        result = employee_schema.dump(employee)
        return jsonify({'message': 'Employee created successfully', 'employee': result}), 201
        
    except IntegrityError as e:
        db.session.rollback()
        print("Exception 3")
        logging.error(f"Database integrity error: {str(e)}")
        return jsonify({'error': 'Database integrity error', 'message': 'Employee number must be unique'}), 409
    
    except SQLAlchemyError as e:
        db.session.rollback()
        print("Exception 4")
        logging.error(f"Database error: {str(e)}")
        return jsonify({'error': 'Database error', 'message': 'Failed to create employee'}), 500
    
    except Exception as e:
        db.session.rollback()
        print("Exception 5")
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/employees', methods=['GET'])
def get_all_employees():
    """Get all employees"""
#    print("get all employees")

    try:
        # Get query parameters for pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Limit per_page to prevent abuse
        per_page = min(per_page, 100)
        
        # Query employees with pagination
        employees = Employee.query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )

        print("Before serialize")
        
        # Serialize employees
        result = employees_schema.dump(employees.items)
        print(result)
        
        return jsonify({
            'employees': result,
            'pagination': {
                'page': employees.page,
                'pages': employees.pages,
                'per_page': employees.per_page,
                'total': employees.total,
                'has_prev': employees.has_prev,
                'has_next': employees.has_next
            }
        }), 200
        
    except SQLAlchemyError as e:
        logging.error(f"Database error: {str(e)}")
        return jsonify({'error': 'Database error', 'message': 'Failed to retrieve employees'}), 500
    
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    """Get a specific employee by ID"""
    try:
        employee = Employee.query.get(employee_id)
        
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404
        
        result = employee_schema.dump(employee)
        return jsonify({'employee': result}), 200
        
    except SQLAlchemyError as e:
        logging.error(f"Database error: {str(e)}")
        return jsonify({'error': 'Database error', 'message': 'Failed to retrieve employee'}), 500
    
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    """Update an existing employee"""
    try:
        # Get the employee
        employee = Employee.query.get(employee_id)
        
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404
        
        # Get JSON data from request
        json_data = request.get_json()
        
        if not json_data:
            return jsonify({'error': 'No input data provided'}), 400
        
        # Validate and deserialize input
        try:
            employee_data = employee_schema.load(json_data)
        except ValidationError as err:
            return jsonify({'error': 'Validation error', 'messages': err.messages}), 400
        
        # Check if employee number already exists (excluding current employee)
        if 'employee_number' in employee_data:
            existing_employee = Employee.query.filter(
                Employee.employee_number == employee_data['employee_number'],
                Employee.id != employee_id
            ).first()
            
            if existing_employee:
                return jsonify({'error': 'Employee number already exists'}), 409
        
        # Update employee fields
        for key, value in employee_data.items():
            setattr(employee, key, value)
        
        db.session.commit()
        
        logging.info(f"Updated employee: {employee.employee_number}")
        
        # Return updated employee
        result = employee_schema.dump(employee)
        return jsonify({'message': 'Employee updated successfully', 'employee': result}), 200
        
    except IntegrityError as e:
        db.session.rollback()
        logging.error(f"Database integrity error: {str(e)}")
        return jsonify({'error': 'Database integrity error', 'message': 'Employee number must be unique'}), 409
    
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"Database error: {str(e)}")
        return jsonify({'error': 'Database error', 'message': 'Failed to update employee'}), 500
    
    except Exception as e:
        db.session.rollback()
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    """Delete an employee"""
    try:
        # Get the employee
        employee = Employee.query.get(employee_id)
        
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404
        
        employee_number = employee.employee_number
        
        # Delete the employee
        db.session.delete(employee)
        db.session.commit()
        
        logging.info(f"Deleted employee: {employee_number}")
        
        return jsonify({'message': 'Employee deleted successfully'}), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"Database error: {str(e)}")
        return jsonify({'error': 'Database error', 'message': 'Failed to delete employee'}), 500
    
    except Exception as e:
        db.session.rollback()
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/employees/by-number/<string:employee_number>', methods=['GET'])
def get_employee_by_number(employee_number):
    """Get a specific employee by employee number"""
    try:
        employee = Employee.query.filter_by(employee_number=employee_number).first()
        
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404
        
        result = employee_schema.dump(employee)
        return jsonify({'employee': result}), 200
        
    except SQLAlchemyError as e:
        logging.error(f"Database error: {str(e)}")
        return jsonify({'error': 'Database error', 'message': 'Failed to retrieve employee'}), 500
    
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Health check endpoint
@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Employee API is running'}), 200
