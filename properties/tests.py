from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from .models import Property


class PropertyImportExportTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(
			username='property-import-user', password='test-password',
		)
		self.client.force_login(self.user)

	def test_csv_upload_map_and_import(self):
		response = self.client.post('/properties/import/', {
			'file': SimpleUploadedFile(
				'properties.csv',
				b'Title,Description,Address,City,State,Zip Code,Price,Square Feet\n'
				b'Villa,Sunny home,1 Main St,Cairo,Cairo,11511,250000,1800\n',
				content_type='text/csv',
			),
		})
		self.assertRedirects(response, '/properties/import/map/')
		response = self.client.post('/properties/import/', {
			'confirm': '1', 'col_0': 'title', 'col_1': 'description',
			'col_2': 'address', 'col_3': 'city', 'col_4': 'state',
			'col_5': 'zip_code', 'col_6': 'price', 'col_7': 'square_feet',
		})
		self.assertRedirects(response, '/properties/')
		property_obj = Property.objects.get(title='Villa')
		self.assertEqual(property_obj.city, 'Cairo')
		self.assertEqual(property_obj.price, 250000)

	def test_invalid_numeric_values_do_not_crash_import(self):
		response = self.client.post('/properties/import/', {
			'file': SimpleUploadedFile(
				'properties.csv',
				b'Title,Address,City,State,Zip Code,Price,Square Feet\n'
				b'Robust Home,1 Main St,Cairo,Cairo,11511,not-a-price,not-a-number\n',
				content_type='text/csv',
			),
		})
		self.assertRedirects(response, '/properties/import/map/')
		response = self.client.post('/properties/import/', {
			'confirm': '1', 'col_0': 'title', 'col_1': 'address',
			'col_2': 'city', 'col_3': 'state', 'col_4': 'zip_code',
			'col_5': 'price', 'col_6': 'square_feet',
		})
		self.assertEqual(response.status_code, 302)
		self.assertTrue(Property.objects.filter(title='Robust Home').exists())

	def test_import_matches_existing_title_without_case_sensitivity(self):
		property_obj = Property.objects.create(
			title='Existing Villa', description='Old description', address='1 Main St',
			city='Cairo', state='Cairo', zip_code='11511', square_feet=1000, price=100000,
		)
		response = self.client.post('/properties/import/', {
			'file': SimpleUploadedFile(
				'properties.csv',
				b'Title,Price,External Reference\n existing villa ,250000,CRM-42\n',
				content_type='text/csv',
			),
		})
		self.assertRedirects(response, '/properties/import/map/')
		response = self.client.get('/properties/import/map/')
		self.assertContains(response, 'Needs mapping')
		response = self.client.post('/properties/import/', {
			'confirm': '1', 'col_0': 'title', 'col_1': 'price',
		})
		self.assertRedirects(response, '/properties/')
		self.assertEqual(Property.objects.count(), 1)
		property_obj.refresh_from_db()
		self.assertEqual(property_obj.price, 250000)

	def test_export_endpoints_return_files(self):
		Property.objects.create(
			title='Export Home', description='Home', address='1 Main St', city='Cairo',
			state='Cairo', zip_code='11511', square_feet=1000, price=100000,
		)
		csv_response = self.client.get('/properties/export/csv/')
		excel_response = self.client.get('/properties/export/excel/')
		self.assertEqual(csv_response.status_code, 200)
		self.assertEqual(csv_response['Content-Type'], 'text/csv; charset=utf-8')
		self.assertEqual(excel_response.status_code, 200)
		self.assertIn('spreadsheetml', excel_response['Content-Type'])
