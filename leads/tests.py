from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Lead, LeadCall, LeadEmail, LeadMeeting, LeadNote, LeadSavedFilter, LeadTask

class LeadImportTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(
			username='import-user',
			password='test-password',
		)
		self.client.force_login(self.user)

	def import_csv(self, content, mapping):
		response = self.client.post(
			'/leads/import/',
			{'file': SimpleUploadedFile('leads.csv', content.encode(), content_type='text/csv')},
		)
		self.assertEqual(response.status_code, 302)
		return self.client.post('/leads/import/', {'confirm': '1', **mapping})

	def test_import_accepts_only_first_name_and_email(self):
		response = self.import_csv(
			'First Name,Email\nAda,ada-only@example.com\n',
			{'col_0': 'first_name', 'col_1': 'email'},
		)

		self.assertRedirects(response, '/leads/')
		lead = Lead.objects.get(email='ada-only@example.com')
		self.assertEqual(lead.first_name, 'Ada')
		self.assertEqual(lead.last_name, '')
		self.assertEqual(lead.phone, '')

	def test_import_does_not_require_lead_fields(self):
		response = self.import_csv(
			'Phone\n555-0100\n',
			{'col_0': 'phone'},
		)

		self.assertRedirects(response, '/leads/')
		self.assertTrue(Lead.objects.filter(phone='555-0100').exists())

	def test_import_creates_mapped_activities(self):
		headers = ','.join([
			'First Name', 'Email', 'Task Title', 'Call Notes', 'Meeting Title',
			'Meeting Date', 'Email Subject', 'Email Body', 'Note Content',
		])
		values = ','.join([
			'Grace', 'grace-activities@example.com', 'Follow up', 'Connected',
			'Property tour', '2026-09-13 10:00', 'Welcome', 'Thanks for your interest',
			'High priority lead',
		])
		mapping = {f'col_{index}': field for index, field in enumerate([
			'first_name', 'email', 'task_title', 'call_notes', 'meeting_title',
			'meeting_date', 'email_subject', 'email_body', 'note_content',
		])}

		response = self.import_csv(f'{headers}\n{values}\n', mapping)

		self.assertRedirects(response, '/leads/')
		lead = Lead.objects.get(email='grace-activities@example.com')
		self.assertEqual(LeadTask.objects.filter(lead=lead, title='Follow up').count(), 1)
		self.assertEqual(LeadCall.objects.filter(lead=lead, notes='Connected').count(), 1)
		self.assertEqual(LeadMeeting.objects.filter(lead=lead, title='Property tour').count(), 1)
		self.assertEqual(LeadEmail.objects.filter(lead=lead, subject='Welcome').count(), 1)
		self.assertEqual(LeadNote.objects.filter(lead=lead, content='High priority lead').count(), 1)


class LeadSavedFilterTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(
			username='filter-user',
			password='test-password',
		)
		self.client.force_login(self.user)
		Lead.objects.create(
			first_name='Visible',
			email='visible@example.com',
			phone='123',
			priority='high',
		)

	def test_user_can_save_and_restore_named_columns_and_filters(self):
		response = self.client.post('/leads/filters/save/', {
			'name': 'High priority contacts',
			'q': 'Visible',
			'priority': 'high',
			'columns': ['name', 'email', 'actions'],
		})

		saved_filter = LeadSavedFilter.objects.get(user=self.user, name='High priority contacts')
		self.assertRedirects(response, f'/leads/?view={saved_filter.pk}')
		self.assertTrue(saved_filter.is_last_used)
		response = self.client.get('/leads/')
		self.assertContains(response, 'High priority contacts')
		self.assertContains(response, 'name="q"')
		self.assertContains(response, 'visible@example.com')
		self.assertNotContains(response, '<th>Phone</th>', html=False)

	def test_loading_another_view_marks_it_as_last_used(self):
		first = LeadSavedFilter.objects.create(
			user=self.user, name='First', columns=['name'], filters={}, is_last_used=True,
		)
		second = LeadSavedFilter.objects.create(
			user=self.user, name='Second', columns=['email'], filters={}, is_last_used=False,
		)

		self.client.get(f'/leads/?view={second.pk}')

		first.refresh_from_db()
		second.refresh_from_db()
		self.assertFalse(first.is_last_used)
		self.assertTrue(second.is_last_used)
