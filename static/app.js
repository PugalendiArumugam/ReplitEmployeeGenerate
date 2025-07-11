/**
 * Employee API Testing Interface
 */

// Sample data for different request types
const sampleData = {
    POST: {
        "employee_number": "EMP001",
        "employee_name": "John Doe", 
        "employee_dob": "1990-05-15",
        "employee_firstname": "John",
        "employee_lastname": "Doe",
        "employee_city": "New York"
    },
    PUT: {
        "employee_number": "EMP001",
        "employee_name": "John Smith",
        "employee_dob": "1990-05-15", 
        "employee_firstname": "John",
        "employee_lastname": "Smith",
        "employee_city": "Los Angeles"
    }
};

// Update request body when method changes
document.getElementById('method').addEventListener('change', function() {
    const method = this.value;
    const requestBodyTextarea = document.getElementById('requestBody');
    
    if (method === 'POST' || method === 'PUT') {
        requestBodyTextarea.value = JSON.stringify(sampleData[method], null, 2);
        requestBodyTextarea.parentElement.style.display = 'block';
    } else {
        requestBodyTextarea.value = '';
        requestBodyTextarea.parentElement.style.display = 'none';
    }
});

// Update endpoint options based on method
document.getElementById('method').addEventListener('change', function() {
    const method = this.value;
    const endpointSelect = document.getElementById('endpoint');
    
    // Clear existing options
    endpointSelect.innerHTML = '';
    
    let options = [];
    
    switch(method) {
        case 'GET':
            options = [
                {value: '/employees', text: 'All Employees'},
                {value: '/employees/1', text: 'Employee by ID (1)'},
                {value: '/employees/by-number/EMP001', text: 'Employee by Number (EMP001)'},
                {value: '/health', text: 'Health Check'}
            ];
            break;
        case 'POST':
            options = [
                {value: '/employees', text: 'Create Employee'}
            ];
            break;
        case 'PUT':
            options = [
                {value: '/employees/1', text: 'Update Employee (ID: 1)'}
            ];
            break;
        case 'DELETE':
            options = [
                {value: '/employees/1', text: 'Delete Employee (ID: 1)'}
            ];
            break;
    }
    
    options.forEach(option => {
        const optionElement = document.createElement('option');
        optionElement.value = option.value;
        optionElement.textContent = option.text;
        endpointSelect.appendChild(optionElement);
    });
});

/**
 * Test API endpoint
 */
async function testAPI() {
    const method = document.getElementById('method').value;
    const endpoint = document.getElementById('endpoint').value;
    const baseUrl = document.getElementById('apiUrl').value;
    const requestBody = document.getElementById('requestBody').value;
    const responseDiv = document.getElementById('response');
    const responseData = document.getElementById('responseData');
    
    try {
        const url = baseUrl + endpoint;
        
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            }
        };
        
        // Add request body for POST and PUT requests
        if ((method === 'POST' || method === 'PUT') && requestBody.trim()) {
            try {
                // Validate JSON
                JSON.parse(requestBody);
                options.body = requestBody;
            } catch (e) {
                throw new Error('Invalid JSON in request body');
            }
        }
        
        // Show loading state
        responseData.textContent = 'Loading...';
        responseDiv.style.display = 'block';
        
        const response = await fetch(url, options);
        const data = await response.json();
        
        // Format response
        const formattedResponse = {
            status: response.status,
            statusText: response.statusText,
            headers: {
                'content-type': response.headers.get('content-type')
            },
            data: data
        };
        
        responseData.textContent = JSON.stringify(formattedResponse, null, 2);
        
        // Add color coding based on status
        if (response.ok) {
            responseData.className = 'bg-success text-white p-3 rounded';
        } else {
            responseData.className = 'bg-danger text-white p-3 rounded';
        }
        
    } catch (error) {
        responseData.textContent = `Error: ${error.message}`;
        responseData.className = 'bg-danger text-white p-3 rounded';
        responseDiv.style.display = 'block';
    }
}

// Initialize the interface
document.addEventListener('DOMContentLoaded', function() {
    // Trigger method change to set initial state
    document.getElementById('method').dispatchEvent(new Event('change'));
});

/**
 * Utility function to format JSON
 */
function formatJSON(obj) {
    return JSON.stringify(obj, null, 2);
}

/**
 * Copy response to clipboard
 */
function copyResponse() {
    const responseText = document.getElementById('responseData').textContent;
    navigator.clipboard.writeText(responseText).then(function() {
        // Show success message
        const originalText = document.querySelector('.copy-btn').textContent;
        document.querySelector('.copy-btn').textContent = 'Copied!';
        setTimeout(() => {
            document.querySelector('.copy-btn').textContent = originalText;
        }, 2000);
    });
}
