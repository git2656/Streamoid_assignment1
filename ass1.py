# 1. IMPORTS GO AT THE TOP
from flask import Flask, request, jsonify
from models import db, Product
import csv
import io

# 2. APP SETUP
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create the database tables if they don't exist
with app.app_context():
    db.create_all()

# 3. API ROUTES ARE DEFINED AFTER THE APP IS CREATED

# API: POST /upload
@app.route('/upload', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        # Read the file in memory to avoid saving it to disk
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        # Use DictReader to read CSV rows as dictionaries
        csv_input = csv.DictReader(stream)

        stored_count = 0
        failed_entries = []
        line_num = 1 # Start at 1 for header row

        for row in csv_input:
            line_num += 1
            is_valid = True
            error_reason = ""
            
            # --- VALIDATION LOGIC ---
            required_fields = ['sku', 'name', 'brand', 'mrp', 'price', 'quantity']
            if not all(field in row and row[field] is not None and row[field].strip() != '' for field in required_fields):
                is_valid = False
                error_reason = "Missing one or more required fields (sku, name, brand, mrp, price, quantity)"
            else:
                try:
                    price = float(row['price'])
                    mrp = float(row['mrp'])
                    quantity = int(row['quantity'])

                    # Rule: price must be <= mrp
                    if not (price <= mrp):
                        is_valid = False
                        error_reason = f"Validation failed: Price ({price}) cannot be greater than MRP ({mrp})"
                    
                    # Rule: quantity >= 0
                    if not (quantity >= 0):
                        is_valid = False
                        error_reason = f"Validation failed: Quantity ({quantity}) cannot be negative"
                
                except (ValueError, TypeError):
                    is_valid = False
                    error_reason = "Invalid data type for price, mrp, or quantity. They must be numbers."

            # --- DATABASE STORAGE ---
            if is_valid:
                # Check if SKU already exists to prevent duplicates which would cause an error
                if not Product.query.get(row['sku']):
                    product = Product(
                        sku=row['sku'],
                        name=row['name'],
                        brand=row['brand'],
                        color=row.get('color'),
                        size=row.get('size'),
                        mrp=mrp,
                        price=price,
                        quantity=quantity
                    )
                    db.session.add(product)
                    stored_count += 1
                else:
                    # SKU already exists, so it's a failed entry
                    failed_entries.append({"row_number": line_num, "data": row, "error": "Duplicate SKU"})
            else:
                # If validation failed, add it to the list of failed entries
                failed_entries.append({"row_number": line_num, "data": row, "error": error_reason})

        # Commit all the valid new products to the database at once
        db.session.commit()
        return jsonify({"stored": stored_count, "failed": failed_entries})

    return jsonify({"error": "File processing failed"}), 500

# API: GET /products
@app.route('/products', methods=['GET'])
def get_products():
    # Get page and limit from query parameters, with default values if not provided
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    # Calculate offset for pagination
    offset = (page - 1) * limit
    
    products = Product.query.limit(limit).offset(offset).all()
    
    # Convert product objects to a list of dictionaries for the JSON response
    result = [p.to_dict() for p in products]
    
    return jsonify(result)

# API: GET /products/search
@app.route('/products/search', methods=['GET'])
def search_products():
    # Start with a query for all products, then chain filters onto it
    query = Product.query

    # Apply filters based on query parameters if they exist in the URL
    if 'brand' in request.args:
        query = query.filter_by(brand=request.args['brand'])
    
    if 'color' in request.args:
        query = query.filter_by(color=request.args['color'])

    if 'minPrice' in request.args:
        query = query.filter(Product.price >= float(request.args['minPrice']))
        
    if 'maxPrice' in request.args:
        query = query.filter(Product.price <= float(request.args['maxPrice']))
        
    products = query.all()
    result = [p.to_dict() for p in products]
    
    return jsonify(result)

# 4. RUN THE APP
if __name__ == '__main__':
    # Use port 8000 as specified in the exercise example
    app.run(debug=True, port=8000)

