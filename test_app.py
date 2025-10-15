import unittest
import json
from ass2 import app, db, Product
from io import BytesIO

class ProductApiTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_upload_and_list_products(self):
        csv_data = (
            b"sku,name,brand,color,size,mrp,price,quantity\n"
            b"TEST-001,Test T-Shirt,TestBrand,Red,M,1000,500,10\n"
            b"TEST-002,Invalid Price,TestBrand,Blue,L,800,900,5\n"
        )
        data = {'file': (BytesIO(csv_data), 'products.csv')}
        response = self.app.post('/upload', content_type='multipart/form-data', data=data)
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.data)
        self.assertEqual(json_response['stored'], 1)
        self.assertEqual(len(json_response['failed']), 1)
        
        response = self.app.get('/products')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['sku'], 'TEST-001')

    def test_search_product(self):
        product = Product(sku='SEARCH-001', name='Searchable Jean', brand='SearchBrand', mrp=2000, price=1500, quantity=20)
        with app.app_context():
            db.session.add(product)
            db.session.commit()
        
        response = self.app.get('/products/search?brand=SearchBrand')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['sku'], 'SEARCH-001')

if __name__ == '__main__':
    unittest.main()
