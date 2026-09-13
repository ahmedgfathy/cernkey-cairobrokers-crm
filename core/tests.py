import io

from django.contrib.auth import get_user_model
from django.test import TestCase

from .import_export import auto_match_headers, parse_uploaded_file


class ImportExportTests(TestCase):
	def test_auto_match_headers_normalizes_column_names(self):
		fields = {
			'first_name': 'First Name',
			'last_name': 'Last Name',
			'email': 'Email',
		}

		mapping = auto_match_headers(
			['first-name', ' LAST_NAME ', 'email'],
			fields,
		)

		self.assertEqual(mapping, {
			0: 'first_name',
			1: 'last_name',
			2: 'email',
		})

	def test_parse_uploaded_csv_returns_headers_and_rows(self):
		uploaded_file = io.BytesIO(
			b'First Name,Email\nAda,ada@example.com\n'
		)
		uploaded_file.name = 'leads.csv'

		headers, rows = parse_uploaded_file(uploaded_file)

		self.assertEqual(headers, ['First Name', 'Email'])
		self.assertEqual(rows, [['Ada', 'ada@example.com']])


class LanguageSwitchTests(TestCase):
	def test_arabic_language_switch_renders_rtl_shell(self):
		user = get_user_model().objects.create_user(username='language-user')
		self.client.force_login(user)

		response = self.client.post('/i18n/setlang/', {
			'language': 'ar',
			'next': '/leads/',
		})

		self.assertRedirects(response, '/leads/')
		response = self.client.get('/leads/')
		self.assertContains(response, '<html lang="ar" dir="rtl">', html=False)
		self.assertContains(response, 'العملاء المحتملون')
