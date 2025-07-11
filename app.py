import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Enable CORS for all routes
CORS(app)

# Configure the database - Use MySQL by default with fallback
mysql_url = os.environ.get("MYSQL_DATABASE_URL")
if mysql_url:
    database_url = mysql_url
else:
    # Fallback to PostgreSQL if MySQL URL not provided
    database_url = os.environ.get("DATABASE_URL", "mysql+pymysql://root:password@localhost/employee_db")

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the app with the extension
db.init_app(app)

with app.app_context():
    # Import models to ensure tables are created
    from models import Employee
    from routes import api_bp
    
    # Register blueprints
    app.register_blueprint(api_bp)
    
    # Create all tables
    db.create_all()
    logging.info("Database tables created successfully")

# Index route for API documentation
@app.route('/')
def index():
    from flask import render_template
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
