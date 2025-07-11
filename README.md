# Employee REST API

A complete Flask-based REST API for employee management with full CRUD operations and MySQL database support.

## Features

- **Complete CRUD Operations**: Create, Read, Update, Delete employees
- **MySQL Database Support**: Optimized for MySQL with connection pooling
- **Data Validation**: Comprehensive input validation with detailed error messages
- **REST API Design**: Following REST conventions with proper HTTP status codes
- **Interactive Documentation**: Built-in web interface for API testing
- **Pagination Support**: Efficient handling of large employee datasets
- **Error Handling**: Robust error handling with meaningful responses

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/employees` | Create a new employee |
| GET | `/api/v1/employees` | Get all employees (paginated) |
| GET | `/api/v1/employees/{id}` | Get employee by ID |
| GET | `/api/v1/employees/by-number/{number}` | Get employee by employee number |
| PUT | `/api/v1/employees/{id}` | Update employee by ID |
| DELETE | `/api/v1/employees/{id}` | Delete employee by ID |
| GET | `/api/v1/health` | Health check endpoint |

## Employee Data Model

```json
{
  "employee_number": "EMP001",
  "employee_name": "John Doe",
  "employee_dob": "1990-05-15",
  "employee_firstname": "John",
  "employee_lastname": "Doe",
  "employee_city": "New York"
}
```

### Field Specifications

- `employee_number`: Unique identifier (String, required, alphanumeric + hyphens)
- `employee_name`: Full name (String, required)
- `employee_dob`: Date of birth (Date, YYYY-MM-DD format, required)
- `employee_firstname`: First name (String, required, min 2 chars)
- `employee_lastname`: Last name (String, required, min 2 chars)
- `employee_city`: City of residence (String, required)

## Setup Instructions

### Prerequisites

- Python 3.11+
- MySQL database
- pip or uv package manager

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd employee-rest-api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
# or using uv
uv sync
```

3. Configure environment variables:
```bash
export MYSQL_DATABASE_URL="mysql+pymysql://username:password@host:port/database"
export SESSION_SECRET="your-secret-key"
```

4. Run the application:
```bash
python main.py
```

The API will be available at `http://localhost:5000`

## Database Configuration

### MySQL Connection String Format
```
mysql+pymysql://username:password@host:port/database_name
```

### Environment Variables
- `MYSQL_DATABASE_URL`: Primary MySQL connection string
- `DATABASE_URL`: Fallback database URL (supports PostgreSQL)
- `SESSION_SECRET`: Secret key for session management

## Usage Examples

### Create Employee
```bash
curl -X POST http://localhost:5000/api/v1/employees \
  -H "Content-Type: application/json" \
  -d '{
    "employee_number": "EMP001",
    "employee_name": "John Doe",
    "employee_dob": "1990-05-15",
    "employee_firstname": "John",
    "employee_lastname": "Doe",
    "employee_city": "New York"
  }'
```

### Get All Employees
```bash
curl http://localhost:5000/api/v1/employees?page=1&per_page=10
```

### Get Employee by ID
```bash
curl http://localhost:5000/api/v1/employees/1
```

### Update Employee
```bash
curl -X PUT http://localhost:5000/api/v1/employees/1 \
  -H "Content-Type: application/json" \
  -d '{
    "employee_number": "EMP001",
    "employee_name": "John Smith",
    "employee_dob": "1990-05-15",
    "employee_firstname": "John",
    "employee_lastname": "Smith",
    "employee_city": "Los Angeles"
  }'
```

### Delete Employee
```bash
curl -X DELETE http://localhost:5000/api/v1/employees/1
```

## Interactive Documentation

Visit `http://localhost:5000` in your browser to access the interactive API documentation and testing interface.

## Project Structure

```
├── app.py              # Main application configuration
├── main.py             # Application entry point
├── models.py           # Employee database model
├── routes.py           # API route definitions
├── serializers.py      # Data validation schemas
├── templates/
│   └── index.html      # Interactive documentation
├── static/
│   └── app.js          # Frontend testing interface
├── pyproject.toml      # Python dependencies
└── README.md           # This file
```

## Error Handling

The API provides comprehensive error handling with appropriate HTTP status codes:

- `200 OK`: Successful operation
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid input data or validation errors
- `404 Not Found`: Resource not found
- `409 Conflict`: Duplicate employee number
- `500 Internal Server Error`: Server-side errors

## Features

### Data Validation
- Employee number format validation
- Date of birth validation (age between 16-100 years)
- Required field validation
- Unique constraint enforcement

### Database Features
- Automatic table creation
- Connection pooling for performance
- Transaction management with rollback
- Audit timestamps (created_at, updated_at)

### API Features
- CORS enabled for frontend integration
- Pagination support for large datasets
- Comprehensive logging for debugging
- Health check endpoint for monitoring

## Testing with Postman

1. Import the base URL: `http://localhost:5000/api/v1`
2. Set Content-Type header to `application/json` for POST/PUT requests
3. Use the example JSON payloads provided above
4. Check the interactive documentation for sample requests

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues and questions, please create an issue in the GitHub repository.# ReplitEmployeeGenerate
# ReplitEmployeeGenerate
