# Streamoid_assignment1
Product Catalog Backend Service
This is a backend service built with Flask that allows users to upload a CSV file of product data, validates it, stores it in a database, and provides APIs to list and search the products.

This project was created as a take-home exercise and includes all primary requirements as well as bonus features like unit tests and a Dockerized solution.

Features
CSV Upload: Accepts a products.csv file via a POST request.

Data Validation: Validates each row for required fields, data types, and business rules (price <= mrp, quantity >= 0).

Database Storage: Stores valid products in an SQLite database.

Paginated Listing: GET /products endpoint to list all products with pagination support.

Product Search: GET /products/search endpoint to filter products by brand, color, and price range (minPrice, maxPrice).

Unit Tests: Includes a test suite to validate API functionality.

Docker Support: Comes with a Dockerfile for easy setup and deployment in any environment.

API Documentation
1. Upload Products from CSV
Uploads a CSV file, processes it, and stores valid products in the database.

Endpoint: /upload

Method: POST

Request: multipart/form-data with a file field named file.

Sample Request (curl):

curl -X POST -F "file=@products.csv" http://localhost:8000/upload

Sample Success Response:

{
  "stored": 20,
  "failed": []
}

2. List All Products
Retrieves a paginated list of all products stored in the database.

Endpoint: /products

Method: GET

Query Parameters:

page (optional, default: 1): The page number to retrieve.

limit (optional, default: 10): The number of products per page.

Sample Request (curl):

# Get the first 5 products
curl "http://localhost:8000/products?limit=5"

Sample Response:

[
    {
        "sku": "TSHIRT-RED-001",
        "name": "Classic Cotton T-Shirt",
        "brand": "Stream Threads",
        "color": "Red",
        "size": "M",
        "mrp": 799.0,
        "price": 499.0,
        "quantity": 20
    }
]

3. Search Products
Retrieves a list of products that match the specified filter criteria.

Endpoint: /products/search

Method: GET

Query Parameters:

brand (optional): Filter by brand name (e.g., DenimWorks).

color (optional): Filter by color (e.g., Red).

minPrice (optional): Filter for products with a price greater than or equal to this value.

maxPrice (optional): Filter for products with a price less than or equal to this value.

Sample Request (curl):

# Search for products from BloomWear that cost 2500 or less
curl "http://localhost:8000/products/search?brand=BloomWear&maxPrice=2500"

Setup and Testing Instructions
There are two ways to run this project: locally with a Python environment, or using Docker.

Option 1: Running Locally
Prerequisites:

Python 3.10+

pip

Instructions:

Clone the repository:

git clone <your-repo-url>
cd <repository-folder>

Create and activate a virtual environment:

# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

Install the required dependencies:

pip install -r requirements.txt

Run the Flask application:

python ass2.py

The server will be running at http://localhost:8000.

Option 2: Running with Docker (Recommended)
Prerequisites:

Docker Desktop installed and running.

Instructions:

Clone the repository as shown above.

Build the Docker image from the root of the project:

docker build -t product-catalog-app .

Run the Docker container:

docker run -p 8000:8000 product-catalog-app

The server will be running inside the container and accessible at http://localhost:8000.

Running the Unit Tests
To verify the functionality of the APIs, you can run the provided unit tests.

Follow the "Running Locally" setup instructions first.

Run the test script:

python test_app.py
