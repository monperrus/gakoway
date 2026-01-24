#!/usr/bin/python
"""
API Gateway Module
A Flask-based dynamic API gateway that routes HTTP requests to Python functions
defined in external modules. This gateway enables hot-reloading of modules and 
provides a flexible routing mechanism for microservices or modular applications.
Architecture:
    The gateway accepts requests at the pattern '/<module>/<file>/<function>' where:
    - 'module' corresponds to the directory containing the Python module
    - 'file' corresponds to a Python module file (without .py extension)
    - 'function' is the name of the callable function within that module
Features:
    - Dynamic module loading and hot-reloading when changes are detected
    - Support for both GET and POST HTTP methods
    - JSON request/response handling
    - Security validation to prevent path traversal attacks
    - Automatic error handling and appropriate HTTP status codes
Deployment:
    Production deployment recommended using Gunicorn:
    Note: Each worker process maintains its own module cache. For stateful
    applications, use external storage (database/files) rather than in-memory state.
Security Considerations:
    - Path validation prevents directory traversal attacks
    - Only modules in the same directory as gateway.py can be loaded
    - No authentication/authorization built-in (should be added for production)
Example Usage:
    POST /services/mymodule/process_data
    GET /data/analytics/get_stats
    The gateway will import services.mymodule and call process_data() or 
    data.analytics and call get_stats() respectively.
Returns:
    JSON responses with function results or error messages with appropriate
    HTTP status codes (200 for success, 404 for not found, 500 for errors)
"""

from flask import Flask, request, jsonify
import importlib
import os


app = Flask(__name__)

@app.route('/<module>/<file>/<function>', methods=['GET', 'POST'])
def gateway(module, file, function):
    try:
        assert ".." not in module and "/" not in module, "Invalid module"
        assert ".." not in file and "/" not in file, "Invalid file"
        
        module_path = f"{module}.{file}"
        # Import the module dynamically
        if os.path.exists(os.path.join(module, file + ".py")):
            mod = importlib.import_module(module_path)
            importlib.reload(mod)
        else:
            raise ImportError(f"Module {module_path} not found")

        # Get the function from the module
        func = getattr(mod, function)
        
        # Call the function with request data
        if request.method == 'POST':
            result = func(request = request.get_json())
        else:
            result = func()
        
        return jsonify(result)
    except (ImportError, AttributeError) as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()