from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from .models import Product

# Create your tests here.

class AddProductViewTest(TestCase):

    def setUp(self):
        # Create a fake image for testing.
        self.image = SimpleUploadedFile(
            'test_image.jpg',
            b'file_content',
            content_type='image/jpeg'
        )
        # URL for our view (change 'add_product' to your view's URL name in urls.py)
        self.url = reverse('add_product')

    def test_add_product_success(self):
        # Data to send in POST request
        data = {
            'name': 'Test Product',
            'price': '19.99',
            'supplier': 'Test Supplier',
            'expiry_date': '2025-12-31',
            'category': 'Test Category',
            'serial_number': 'ABC123',
        }

        # Send POST request with image file
        response = self.client.post(self.url, data | {'image': self.image}, format='multipart')

        # Check status code
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Product added successfully!", response.content)

        # Check if product is saved in the database
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.first().name, 'Test Product')

    def test_missing_fields(self):
        # Send POST request with missing fields
        data = {
            'name': 'Test Product',
            # Missing price, supplier, expiry_date, etc.
        }
        response = self.client.post(self.url, data)
        
        # Expect an error
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"All fields are required!", response.content)

    def test_get_request(self):
        # Send a GET request instead of POST
        response = self.client.get(self.url)
        
        # Expect "Please submit the form."
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Please submit the form.", response.content)