import random
from datetime import timedelta, date, time
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from faker import Faker

from leads.models import (LeadSource, LeadStatus, Lead, LeadTask, LeadCall,
                          LeadMeeting, LeadEmail, LeadNote)
from properties.models import (PropertyType, PropertyStatus, Property,
                                PropertyUnit, PropertyViewing, PropertyOffer,
                                PropertyNote)
from opportunities.models import OpportunityStage, Opportunity
from tasks.models import TaskCategory, TaskPriority, TaskStatus, Task
from notifications.models import NotificationType, Notification
from documents.models import DocumentType, Document

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = 'Seed database with fake data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # Create users
        users = self._create_users()
        admin_user = users[0]

        # Reference data
        lead_sources = self._create_lead_sources()
        lead_statuses = self._create_lead_statuses()
        property_types = self._create_property_types()
        property_statuses = self._create_property_statuses()
        opp_stages = self._create_opportunity_stages()
        task_categories = self._create_task_categories()
        task_priorities = self._create_task_priorities()
        task_statuses = self._create_task_statuses()
        notif_types = self._create_notification_types()
        doc_types = self._create_document_types()

        # Main data
        leads = self._create_leads(lead_sources, lead_statuses, users)
        properties = self._create_properties(property_types, property_statuses, users)
        opportunities = self._create_opportunities(opp_stages, leads, properties, users)
        self._create_tasks(task_categories, task_priorities, task_statuses, leads, properties, opportunities, users)
        self._create_notifications(notif_types, users, leads, properties, opportunities)
        self._create_documents(doc_types, users, leads, properties, opportunities)
        self._create_lead_activities(leads, users)
        self._create_property_activities(properties, users)

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))

    def _create_users(self):
        users = []
        # Admin
        if not User.objects.filter(username='admin').exists():
            u = User.objects.create_superuser('admin', 'admin@cairobrokers.com', 'admin123',
                                               user_type='admin', first_name='Admin', last_name='User')
            users.append(u)
        else:
            users.append(User.objects.get(username='admin'))

        user_data = [
            ('jsmith', 'James', 'Smith', 'agent', '555-0101'),
            ('mjohnson', 'Maria', 'Johnson', 'agent', '555-0102'),
            ('rwilson', 'Robert', 'Wilson', 'agent', '555-0103'),
            ('sbrown', 'Sarah', 'Brown', 'agent', '555-0104'),
            ('dlee', 'David', 'Lee', 'manager', '555-0105'),
            ('lgarcia', 'Linda', 'Garcia', 'agent', '555-0106'),
            ('kmartinez', 'Kevin', 'Martinez', 'agent', '555-0107'),
            ('janderson', 'Jennifer', 'Anderson', 'agent', '555-0108'),
            ('mthomas', 'Michael', 'Thomas', 'manager', '555-0109'),
            ('ewhite', 'Emily', 'White', 'agent', '555-0110'),
        ]
        for uname, first, last, utype, phone in user_data:
            if not User.objects.filter(username=uname).exists():
                u = User.objects.create_user(uname, f'{uname}@cairobrokers.com', 'pass1234',
                                             user_type=utype, first_name=first, last_name=last, phone=phone)
                users.append(u)
            else:
                users.append(User.objects.get(username=uname))

        self.stdout.write(f'  Created {len(users)} users')
        return users

    def _create_lead_sources(self):
        sources_data = [
            ('Website', 'Inquiries from the company website'),
            ('Referral', 'Client referrals'),
            ('Social Media', 'Leads from social platforms'),
            ('Walk-in', 'Walk-in inquiries'),
            ('Phone Call', 'Inbound phone inquiries'),
            ('Email Campaign', 'Marketing email campaigns'),
            ('Zillow', 'Zillow listing inquiries'),
            ('Realtor.com', 'Realtor.com leads'),
            ('Open House', 'Open house attendees'),
            ('LinkedIn', 'LinkedIn outreach'),
            ('Google Ads', 'Google advertising campaigns'),
            ('Facebook Ads', 'Facebook advertising'),
            ('Property Exhibition', 'Real estate expo attendees'),
            ('Cold Call', 'Outbound cold calls'),
            ('Partner Network', 'Partner agency referrals'),
        ]
        objs = []
        for name, desc in sources_data:
            obj, _ = LeadSource.objects.get_or_create(name=name, defaults={'description': desc})
            objs.append(obj)
        self.stdout.write(f'  Created {len(objs)} lead sources')
        return objs

    def _create_lead_statuses(self):
        statuses_data = [
            ('New', '#007bff', 'Fresh lead, not yet contacted'),
            ('Contacted', '#17a2b8', 'Initial contact made'),
            ('Qualified', '#28a745', 'Lead meets criteria'),
            ('Proposal Sent', '#ffc107', 'Proposal has been sent'),
            ('Negotiation', '#fd7e14', 'In active negotiation'),
            ('Closed Won', '#20c997', 'Successfully closed'),
            ('Closed Lost', '#dc3545', 'Did not convert'),
            ('On Hold', '#6c757d', 'Paused temporarily'),
            ('Unqualified', '#343a40', 'Does not meet criteria'),
            ('Nurturing', '#6f42c1', 'Long-term nurture campaign'),
        ]
        objs = []
        for name, color, desc in statuses_data:
            obj, _ = LeadStatus.objects.get_or_create(name=name, defaults={'color': color, 'description': desc})
            objs.append(obj)
        self.stdout.write(f'  Created {len(objs)} lead statuses')
        return objs

    def _create_property_types(self):
        types_data = [
            ('Apartment', 'Multi-unit residential building'),
            ('House', 'Single-family detached home'),
            ('Condominium', 'Individual unit in a larger building'),
            ('Townhouse', 'Multi-floor home sharing walls'),
            ('Villa', 'Luxury detached residence'),
            ('Studio', 'Single-room living space'),
            ('Penthouse', 'Top-floor luxury unit'),
            ('Loft', 'Open-plan industrial conversion'),
            ('Duplex', 'Two-story residential unit'),
            ('Commercial Office', 'Office space for businesses'),
            ('Retail Space', 'Commercial retail unit'),
            ('Warehouse', 'Industrial storage facility'),
        ]
        objs = []
        for name, desc in types_data:
            obj, _ = PropertyType.objects.get_or_create(name=name, defaults={'description': desc})
            objs.append(obj)
        self.stdout.write(f'  Created {len(objs)} property types')
        return objs

    def _create_property_statuses(self):
        statuses_data = [
            ('For Sale', '#28a745', 'Available for purchase'),
            ('For Rent', '#007bff', 'Available for lease'),
            ('Sold', '#dc3545', 'Property has been sold'),
            ('Rented', '#6c757d', 'Currently leased'),
            ('Under Contract', '#ffc107', 'Sale in progress'),
            ('Pending', '#fd7e14', 'Awaiting closure'),
            ('Off Market', '#343a40', 'Not currently listed'),
            ('Coming Soon', '#6f42c1', 'Will be listed soon'),
        ]
        objs = []
        for name, color, desc in statuses_data:
            obj, _ = PropertyStatus.objects.get_or_create(name=name, defaults={'color': color, 'description': desc})
            objs.append(obj)
        self.stdout.write(f'  Created {len(objs)} property statuses')
        return objs

    def _create_opportunity_stages(self):
        stages_data = [
            ('Lead Identified', '#6c757d', 'Initial lead captured', 10, 1),
            ('Initial Contact', '#007bff', 'First contact established', 20, 2),
            ('Needs Analysis', '#17a2b8', 'Understanding client needs', 35, 3),
            ('Proposal', '#ffc107', 'Proposal presented', 50, 4),
            ('Negotiation', '#fd7e14', 'Active negotiations', 70, 5),
            ('Contract', '#e83e8c', 'Contract phase', 85, 6),
            ('Closed Won', '#28a745', 'Deal successfully closed', 100, 7),
            ('Closed Lost', '#dc3545', 'Deal lost', 0, 8),
        ]
        objs = []
        for name, color, desc, prob, order in stages_data:
            obj, _ = OpportunityStage.objects.get_or_create(name=name, defaults={
                'color': color, 'description': desc, 'probability': prob, 'order': order
            })
            objs.append(obj)
        self.stdout.write(f'  Created {len(objs)} opportunity stages')
        return objs

    def _create_task_categories(self):
        cats_data = [
            ('Follow-up', '#007bff', 'Follow-up calls and emails'),
            ('Property Viewing', '#28a745', 'Schedule and conduct property viewings'),
            ('Documentation', '#6f42c1', 'Prepare and review documents'),
            ('Client Meeting', '#fd7e14', 'In-person or virtual meetings'),
            ('Administrative', '#6c757d', 'General administrative tasks'),
            ('Marketing', '#e83e8c', 'Marketing and promotional activities'),
            ('Legal', '#dc3545', 'Legal review and compliance'),
            ('Financial', '#20c997', 'Financial analysis and reporting'),
            ('Inspection', '#17a2b8', 'Property inspection tasks'),
            ('Closing', '#ffc107', 'Closing process tasks'),
        ]
        objs = []
        for name, color, desc in cats_data:
            obj, _ = TaskCategory.objects.get_or_create(name=name, defaults={'color': color, 'description': desc})
            objs.append(obj)
        self.stdout.write(f'  Created {len(objs)} task categories')
        return objs

    def _create_task_priorities(self):
        priorities_data = [
            ('Low', '#28a745', 'Low priority'),
            ('Medium', '#ffc107', 'Medium priority'),
            ('High', '#fd7e14', 'High priority'),
            ('Critical', '#dc3545', 'Urgent - requires immediate attention'),
        ]
        objs = []
        for name, color, desc in priorities_data:
            obj, _ = TaskPriority.objects.get_or_create(name=name, defaults={'color': color, 'description': desc})
            objs.append(obj)
        self.stdout.write(f'  Created {len(objs)} task priorities')
        return objs

    def _create_task_statuses(self):
        statuses_data = [
            ('To Do', '#6c757d', 'Not yet started'),
            ('In Progress', '#007bff', 'Currently being worked on'),
            ('On Hold', '#ffc107', 'Paused'),
            ('Completed', '#28a745', 'Finished'),
            ('Cancelled', '#dc3545', 'Cancelled'),
            ('Blocked', '#343a40', 'Blocked by dependency'),
        ]
        objs = []
        for name, color, desc in statuses_data:
            obj, _ = TaskStatus.objects.get_or_create(name=name, defaults={'color': color, 'description': desc})
            objs.append(obj)
        self.stdout.write(f'  Created {len(objs)} task statuses')
        return objs

    def _create_notification_types(self):
        types_data = [
            ('Lead Assigned', '#007bff', 'user-plus', 'A new lead has been assigned'),
            ('Task Reminder', '#ffc107', 'clock', 'Upcoming task deadline'),
            ('Opportunity Update', '#28a745', 'handshake', 'Opportunity stage changed'),
            ('Property Listed', '#17a2b8', 'building', 'New property listed'),
            ('Document Uploaded', '#6f42c1', 'file-alt', 'New document available'),
            ('Message', '#fd7e14', 'envelope', 'New message received'),
            ('System Alert', '#dc3545', 'exclamation-triangle', 'System notification'),
            ('Welcome', '#20c997', 'star', 'Welcome to the platform'),
            ('Meeting Scheduled', '#e83e8c', 'calendar', 'Upcoming meeting reminder'),
            ('Report Ready', '#0dcaf0', 'chart-bar', 'Generated report is ready'),
        ]
        objs = []
        for name, color, icon, desc in types_data:
            obj, _ = NotificationType.objects.get_or_create(name=name, defaults={
                'color': color, 'icon': icon, 'description': desc
            })
            objs.append(obj)
        self.stdout.write(f'  Created {len(objs)} notification types')
        return objs

    def _create_document_types(self):
        types_data = [
            ('Contract', 'Legal contracts and agreements'),
            ('Agreement', 'Client agreements'),
            ('ID Verification', 'Identity verification documents'),
            ('Financial Statement', 'Financial documents'),
            ('Property Listing', 'Property listing materials'),
            ('Inspection Report', 'Property inspection reports'),
            ('Appraisal', 'Property appraisal documents'),
            ('Photo', 'Property photos'),
            ('Floor Plan', 'Property floor plans'),
            ('Correspondence', 'Client correspondence'),
            ('Marketing Material', 'Marketing collateral'),
            ('Legal Notice', 'Legal notices and letters'),
        ]
        objs = []
        for name, desc in types_data:
            obj, _ = DocumentType.objects.get_or_create(name=name, defaults={'description': desc})
            objs.append(obj)
        self.stdout.write(f'  Created {len(objs)} document types')
        return objs

    def _create_leads(self, sources, statuses, users):
        agents = [u for u in users if u.user_type in ('agent', 'manager')]
        leads = []
        first_names_m = ['James','Robert','John','Michael','David','William','Richard','Joseph','Thomas','Christopher',
                         'Daniel','Matthew','Anthony','Mark','Steven','Andrew','Joshua','Kevin','Brian','Ryan',
                         'Nathan','Samuel','Benjamin','Gregory','Timothy','Frank','Scott',' Brandon','Jacob','Tyler']
        first_names_f = ['Mary','Patricia','Jennifer','Linda','Barbara','Elizabeth','Susan','Jessica','Sarah','Karen',
                         'Lisa','Nancy','Betty','Margaret','Sandra','Ashley','Dorothy','Kimberly','Emily','Donna']
        last_names = ['Smith','Johnson','Williams','Brown','Jones','Garcia','Miller','Davis','Rodriguez','Martinez',
                      'Hernandez','Lopez','Gonzalez','Wilson','Anderson','Thomas','Taylor','Moore','Jackson','Martin',
                      'Lee','Perez','Thompson','White','Harris','Sanchez','Clark','Ramirez','Lewis','Robinson',
                      'Walker','Young','Allen','King','Wright','Scott','Torres','Nguyen','Hill','Flores',
                      'Green','Adams','Nelson','Baker','Hall','Rivera','Campbell','Mitchell','Carter','Roberts',
                      'Gomez','Phillips','Evans','Turner','Diaz','Parker','Cruz','Edwards','Collins','Reyes']

        companies = ['Tech Corp', 'Global Industries', 'Summit Holdings', 'Pacific Enterprises', 'Metro Development',
                     'Horizon Group', 'Atlas Properties', 'Pinnacle Investments', 'Coastal Holdings', 'Urban Living LLC',
                     'Star Investments', 'First National Realty', 'Sunshine Properties', 'Golden Gate Holdings', '']

        for i in range(120):
            gender = random.choice(['m', 'f'])
            fn = random.choice(first_names_m if gender == 'm' else first_names_f)
            ln = random.choice(last_names)
            lead = Lead(
                first_name=fn,
                last_name=ln,
                email=f'{fn.lower()}.{ln.lower()}{random.randint(1,99)}@{fake.free_email_domain()}',
                phone=fake.phone_number()[:20],
                company=random.choice(companies),
                source=random.choice(sources) if random.random() > 0.15 else None,
                status=random.choice(statuses) if random.random() > 0.1 else None,
                assigned_to=random.choice(agents) if random.random() > 0.2 else None,
                priority=random.choice(['low', 'medium', 'medium', 'medium', 'high']),
                notes=fake.sentence(nb_words=12) if random.random() > 0.5 else '',
                created_by=random.choice(agents),
            )
            lead.save()
            leads.append(lead)

        self.stdout.write(f'  Created {len(leads)} leads')
        return leads

    def _create_properties(self, types, statuses, users):
        agents = [u for u in users if u.user_type in ('agent', 'manager')]
        properties = []
        cities_states = [
            ('New York', 'NY'), ('Los Angeles', 'CA'), ('Chicago', 'IL'), ('Houston', 'TX'),
            ('Phoenix', 'AZ'), ('Philadelphia', 'PA'), ('San Antonio', 'TX'), ('San Diego', 'CA'),
            ('Dallas', 'TX'), ('Austin', 'TX'), ('Miami', 'FL'), ('Seattle', 'WA'),
            ('Denver', 'CO'), ('Boston', 'MA'), ('Nashville', 'TN'), ('Portland', 'OR'),
            ('San Francisco', 'CA'), ('Las Vegas', 'NV'), ('Atlanta', 'GA'), ('Orlando', 'FL'),
        ]
        street_types = ['St', 'Ave', 'Blvd', 'Dr', 'Ln', 'Way', 'Ct', 'Pl']
        street_names = ['Oak', 'Maple', 'Cedar', 'Elm', 'Pine', 'Birch', 'Walnut', 'Spruce',
                        'Main', 'First', 'Second', 'Park', 'Lake', 'Hill', 'River', 'Forest',
                        'Sunset', 'Broadway', 'Highland', 'Valley', 'Spring', 'Meadow', 'Creek', 'Ridge']

        for i in range(110):
            city, state = random.choice(cities_states)
            ptype = random.choice(types)
            pstatus = random.choice(statuses)
            bedrooms = random.randint(1, 5)
            bathrooms = random.randint(1, 4)
            sqft = random.randint(500, 5000)
            price = Decimal(str(random.randint(150000, 2500000)))

            prop = Property(
                title=f'{random.choice(["Beautiful", "Modern", "Spacious", "Luxury", "Charming", "Elegant", "Cozy", "Stunning"])} {ptype.name} in {city}',
                description=fake.paragraph(nb_sentences=4),
                address=f'{random.randint(1, 9999)} {random.choice(street_names)} {random.choice(street_types)}',
                city=city,
                state=state,
                zip_code=f'{random.randint(10000, 99999)}',
                country='USA',
                property_type=ptype,
                status=pstatus,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                square_feet=sqft,
                lot_size=Decimal(str(random.randint(1000, 20000))) if random.random() > 0.3 else None,
                year_built=random.randint(1950, 2025),
                price=price,
                monthly_rent=price * Decimal('0.008') if pstatus and 'rent' in pstatus.name.lower() else None,
                hoa_fee=Decimal(str(random.randint(100, 800))) if random.random() > 0.4 else None,
                has_garage=random.choice([True, False]),
                garage_spaces=random.randint(0, 3) if random.random() > 0.3 else 0,
                has_pool=random.choice([True, False, False]),
                has_garden=random.choice([True, True, False]),
                pet_friendly=random.choice([True, True, False]),
                listed_by=random.choice(agents),
                is_featured=random.random() > 0.85,
                is_active=random.random() > 0.1,
            )
            prop.save()
            properties.append(prop)

        self.stdout.write(f'  Created {len(properties)} properties')
        return properties

    def _create_opportunities(self, stages, leads, properties, users):
        agents = [u for u in users if u.user_type in ('agent', 'manager')]
        active_stages = [s for s in stages if s.name not in ('Closed Won', 'Closed Lost')]
        opps = []
        opp_names = [
            'Downtown Apartment Sale', 'Beachfront Condo Rental', 'Suburban House Purchase',
            'Luxury Villa Lease', 'Office Space Agreement', 'Townhouse Family Move',
            'Investment Property Deal', 'First Home Purchase', 'Penthouse Rental',
            'Commercial Lease Agreement', 'Studio Apartment Rental', 'Duplex Sale',
            'Warehouse Lease', 'Retail Space Agreement', 'Loft Conversion Sale',
            'Garden Apartment Rental', 'Pool Villa Lease', 'City Center Condo',
            'Waterfront Property Deal', 'Mountain Retreat Purchase',
        ]

        for i in range(100):
            stage = random.choice(active_stages)
            lead = random.choice(leads)
            prop = random.choice(properties)
            opp_type = random.choice(['sale', 'rental', 'lease'])
            created = timezone.now() - timedelta(days=random.randint(0, 180))
            expected = created.date() + timedelta(days=random.randint(7, 120))

            opp = Opportunity(
                name=random.choice(opp_names) + f' #{random.randint(100,999)}',
                description=fake.sentence(nb_words=15),
                opportunity_type=opp_type,
                lead=lead,
                related_property=prop,
                stage=stage,
                assigned_to=random.choice(agents),
                estimated_value=Decimal(str(random.randint(100000, 2000000))),
                expected_close_date=expected,
                actual_close_date=expected if stage.name == 'Closed Won' else None,
                probability=stage.probability,
                created_by=random.choice(agents),
                is_active=stage.name not in ('Closed Won', 'Closed Lost'),
            )
            opp.save()
            opps.append(opp)

        self.stdout.write(f'  Created {len(opps)} opportunities')
        return opps

    def _create_tasks(self, categories, priorities, statuses, leads, properties, opportunities, users):
        agents = [u for u in users if u.user_type in ('agent', 'manager')]
        tasks = []
        task_titles = [
            'Follow up with client', 'Schedule property viewing', 'Prepare listing agreement',
            'Review contract terms', 'Send property brochure', 'Conduct market analysis',
            'Update property photos', 'Contact mortgage lender', 'Prepare offer letter',
            'Schedule home inspection', 'Call client for feedback', 'Review closing documents',
            'Send welcome package', 'Update CRM records', 'Prepare comparative market analysis',
            'Schedule final walkthrough', 'Contact insurance provider', 'Verify title documents',
            'Send closing gift', 'Schedule post-closing follow-up', 'Prepare rental agreement',
            'Conduct property appraisal', 'Review HOA documents', 'Schedule open house',
            'Create marketing flyer', 'Update listing description', 'Contact property manager',
            'Verify employment records', 'Prepare disclosure documents', 'Schedule utility transfer',
            'Send thank you note', 'Review escrow instructions', 'Confirm home warranty',
            'Schedule key handover', 'Update property status', 'Contact contractor for repairs',
            'Prepare staging plan', 'Review neighborhood comps', 'Send payment reminder',
            'Schedule annual review', 'Verify tax records', 'Contact title company',
        ]

        for i in range(120):
            category = random.choice(categories)
            priority = random.choice(priorities)
            status = random.choice(statuses)
            created = timezone.now() - timedelta(days=random.randint(0, 90))
            due = created.date() + timedelta(days=random.randint(1, 30))

            task = Task(
                title=random.choice(task_titles),
                description=fake.sentence(nb_words=10) if random.random() > 0.4 else '',
                lead=random.choice(leads) if random.random() > 0.4 else None,
                related_property=random.choice(properties) if random.random() > 0.5 else None,
                opportunity=random.choice(opportunities) if random.random() > 0.6 else None,
                category=category,
                priority=priority,
                status=status,
                assigned_to=random.choice(agents),
                created_by=random.choice(agents),
                due_date=due,
                due_time=time(random.randint(8, 17), random.choice([0, 15, 30, 45])) if random.random() > 0.3 else None,
                start_date=created.date() if random.random() > 0.5 else None,
                end_date=due if random.random() > 0.5 else None,
                is_completed=status.name == 'Completed',
                completed_at=timezone.now() - timedelta(days=random.randint(0, 10)) if status.name == 'Completed' else None,
            )
            task.save()
            tasks.append(task)

        self.stdout.write(f'  Created {len(tasks)} tasks')
        return tasks

    def _create_notifications(self, types, users, leads, properties, opportunities):
        notifs = []
        templates = [
            ('New lead assigned', 'A new lead {lead} has been assigned to you for follow-up.', 'high'),
            ('Task reminder', 'Your task "{task}" is due on {date}.', 'medium'),
            ('Opportunity update', 'The opportunity "{opp}" has moved to the next stage.', 'medium'),
            ('Property listed', 'A new property "{prop}" has been listed in your area.', 'low'),
            ('Document uploaded', 'A new document has been uploaded for your review.', 'low'),
            ('Meeting reminder', 'You have a meeting scheduled with {lead} tomorrow at 10 AM.', 'high'),
            ('Lead response', '{lead} has responded to your email.', 'medium'),
            ('Closing approaching', 'The closing for "{opp}" is in 3 days.', 'urgent'),
            ('Report generated', 'Your monthly performance report is ready.', 'low'),
            ('Welcome message', 'Welcome to Cairobrokers CRM! Start by exploring your dashboard.', 'low'),
        ]

        for i in range(120):
            lead = random.choice(leads)
            prop = random.choice(properties)
            opp = random.choice(opportunities)
            ntype = random.choice(types)
            title, msg_template, priority = random.choice(templates)

            task_titles = ['Follow up with client', 'Schedule property viewing', 'Prepare listing agreement', 'Review contract']
            msg = msg_template.format(
                lead=lead.full_name,
                prop=prop.title[:30],
                opp=opp.name[:30],
                date=date.today(),
                task=random.choice(task_titles),
            )

            notif = Notification(
                recipient=random.choice(users),
                sender=random.choice(users),
                title=title,
                message=msg,
                notification_type=ntype,
                priority=priority,
                related_lead_id=lead.pk if random.random() > 0.5 else None,
                related_property_id=prop.pk if random.random() > 0.6 else None,
                related_opportunity_id=opp.pk if random.random() > 0.7 else None,
                is_read=random.random() > 0.4,
                is_archived=random.random() > 0.9,
            )
            notif.save()
            notifs.append(notif)

        self.stdout.write(f'  Created {len(notifs)} notifications')
        return notifs

    def _create_documents(self, types, users, leads, properties, opportunities):
        docs = []
        doc_titles = [
            'Purchase Agreement', 'Lease Contract', 'Property Disclosure', 'Inspection Report',
            'Appraisal Document', 'Title Insurance', 'Mortgage Pre-approval', 'Client ID Copy',
            'Proof of Income', 'Bank Statement', 'Property Photos Set', 'Floor Plan',
            'HOA Rules', 'Tax Assessment', 'Survey Report', 'Home Warranty Agreement',
            'Closing Checklist', 'Earnest Money Receipt', 'Commission Agreement', 'Agency Agreement',
            'Marketing Brochure', 'Property Video Tour', 'Neighborhood Guide', 'School District Info',
            'Utility Transfer Form', 'Move-in Checklist', 'Move-out Checklist', 'Maintenance Log',
            'Insurance Certificate', 'W-9 Form', '1099 Form', 'Power of Attorney',
        ]

        for i in range(80):
            doc_type = random.choice(types)
            created = timezone.now() - timedelta(days=random.randint(0, 180))

            doc = Document(
                title=random.choice(doc_titles) + f' v{random.randint(1,3)}',
                description=fake.sentence(nb_words=8) if random.random() > 0.3 else '',
                related_lead_id=random.choice(leads).pk if random.random() > 0.4 else None,
                related_property_id=random.choice(properties).pk if random.random() > 0.5 else None,
                related_opportunity_id=random.choice(opportunities).pk if random.random() > 0.6 else None,
                document_type=doc_type,
                file_size=random.randint(10240, 10485760),
                uploaded_by=random.choice(users),
                is_public=random.random() > 0.7,
                requires_login=random.random() > 0.3,
                version=random.randint(1, 3),
            )
            doc.save()
            docs.append(doc)

        self.stdout.write(f'  Created {len(docs)} documents')
        return docs

    def _create_lead_activities(self, leads, users):
        def future_date():
            return date.today() + timedelta(days=random.randint(1, 90))

        def past_date():
            return date.today() - timedelta(days=random.randint(1, 90))

        task_titles = [
            'Follow up on inquiry', 'Send property details', 'Schedule property viewing',
            'Prepare comparative market analysis', 'Send welcome package',
            'Follow up after viewing', 'Check financing pre-approval',
            'Send neighborhood guide', 'Schedule second viewing',
            'Prepare offer documents', 'Check in with client',
            'Send market update report', 'Schedule listing appointment',
            'Review client feedback', 'Update client on negotiations'
        ]
        call_outcomes = ['connected', 'voicemail', 'no_answer', 'callback_requested', 'interested', 'not_interested']
        meeting_types = ['in_person', 'video_call', 'phone', 'open_house']
        meeting_statuses = ['scheduled', 'completed', 'cancelled', 'rescheduled']
        email_subjects = [
            'Property listing recommendations', 'Viewing confirmation',
            'Follow-up from our meeting', 'Market analysis report',
            'New properties matching your criteria', 'Offer update',
            'Thank you for your interest', 'Documents for your review',
            'Neighborhood information', 'Financing options'
        ]
        note_contents = [
            'Client is very interested in downtown properties. Prefers modern style.',
            'Budget increased to $500K after speaking with mortgage broker.',
            'Looking to move within 3 months due to new job.',
            'Has two young children - needs good school district.',
            'Prefers quiet neighborhood, not interested in busy streets.',
            'Investment buyer looking for rental yield above 6%.',
            'Relocating from out of state, needs virtual tour options.',
            'Very particular about natural light and open floor plans.',
            'Wants to sell current home first before buying.',
            'Has a dog - needs a fenced yard.'
        ]

        tasks = []
        calls = []
        meetings = []
        emails = []
        notes = []

        for lead in leads:
            # 2-4 tasks per lead
            for _ in range(random.randint(2, 4)):
                status = random.choice(['pending', 'in_progress', 'completed', 'cancelled'])
                task = LeadTask.objects.create(
                    lead=lead,
                    assigned_to=random.choice(users),
                    title=random.choice(task_titles),
                    description=fake.paragraph(nb_sentences=2),
                    task_type=random.choice(['follow_up', 'meeting', 'call', 'email', 'document', 'other']),
                    priority=random.choice(['low', 'medium', 'high', 'urgent']),
                    status=status,
                    due_date=future_date() if status != 'completed' else past_date(),
                    completed_at=timezone.now() - timedelta(days=random.randint(1, 30)) if status == 'completed' else None,
                )
                tasks.append(task)

            # 1-3 calls per lead
            for _ in range(random.randint(1, 3)):
                call = LeadCall.objects.create(
                    lead=lead,
                    called_by=random.choice(users),
                    duration_minutes=random.randint(3, 45),
                    outcome=random.choice(call_outcomes),
                    notes=fake.sentence(nb_words=15),
                )
                calls.append(call)

            # 1-2 meetings per lead
            for _ in range(random.randint(1, 2)):
                meeting = LeadMeeting.objects.create(
                    lead=lead,
                    organized_by=random.choice(users),
                    title=random.choice([
                        'Property viewing', 'Needs assessment meeting',
                        'Contract review', 'Market consultation',
                        'Open house follow-up', 'Second viewing'
                    ]),
                    meeting_date=timezone.now() - timedelta(days=random.randint(1, 30)),
                    location=fake.address(),
                    status=random.choice(meeting_statuses),
                    notes=fake.sentence(nb_words=10),
                )
                meetings.append(meeting)

            # 1-3 emails per lead
            for _ in range(random.randint(1, 3)):
                email = LeadEmail.objects.create(
                    lead=lead,
                    sent_by=random.choice(users),
                    subject=random.choice(email_subjects),
                    body=fake.paragraph(nb_sentences=3),
                    direction=random.choice(['incoming', 'outgoing']),
                )
                emails.append(email)

            # 1-2 notes per lead
            for _ in range(random.randint(1, 2)):
                note = LeadNote.objects.create(
                    lead=lead,
                    created_by=random.choice(users),
                    content=random.choice(note_contents),
                )
                notes.append(note)

        self.stdout.write(f'  Created {len(tasks)} lead tasks, {len(calls)} calls, {len(meetings)} meetings, {len(emails)} emails, {len(notes)} notes')

    def _create_property_activities(self, properties, users):
        def future_date():
            return date.today() + timedelta(days=random.randint(1, 90))

        unit_statuses = ['available', 'occupied', 'reserved', 'maintenance']
        viewing_statuses = ['scheduled', 'completed', 'cancelled', 'no_show']
        offer_statuses = ['pending', 'accepted', 'rejected', 'countered', 'withdrawn']
        note_contents = [
            'Property gets excellent natural light in the mornings.',
            'Recently renovated kitchen with modern appliances.',
            'Street parking only - no garage available.',
            'HOA fee includes water and garbage.',
            'Roof replaced in 2022, all major systems updated.',
            'Corner lot with extra outdoor space.',
            'Building has elevator access and wheelchair accessibility.',
            'Great rental history - current tenant lease expires next month.',
            'Walking distance to public transit and shopping.',
            'Noise level is low - great for families.',
            'Property taxes increased this year - factor into pricing.',
            'Previous inspection showed minor foundation crack - monitor.',
            'Solar panels owned outright, not leased.',
            'Pool and gym access included in HOA.',
            'Pets allowed with $500 deposit.'
        ]

        units = []
        viewings = []
        offers = []
        notes = []

        for prop in properties:
            # 1-4 units per property
            num_units = random.randint(1, 4) if prop.property_type and 'condo' in str(prop.property_type).lower() else random.randint(0, 2)
            for i in range(num_units):
                unit = PropertyUnit.objects.create(
                    related_property=prop,
                    unit_number=f'{chr(65 + i)}{random.randint(1, 20):02d}',
                    floor=str(random.randint(1, 30)),
                    square_feet=random.randint(400, 2500),
                    monthly_rent=Decimal(str(round(random.uniform(800, 5000), 2))),
                    sale_price=prop.price + Decimal(str(random.randint(-50000, 100000))) if prop.price else None,
                    bedrooms=random.choice([0, 1, 1, 2, 2, 3]),
                    bathrooms=random.choice([1, 1, 2, 2]),
                    status=random.choice(unit_statuses),
                    description=fake.paragraph(nb_sentences=1),
                )
                units.append(unit)

            # 1-3 viewings per property
            for _ in range(random.randint(1, 3)):
                viewing = PropertyViewing.objects.create(
                    related_property=prop,
                    agent=random.choice(users),
                    prospect_name=fake.name(),
                    prospect_email=fake.email(),
                    prospect_phone=fake.phone_number(),
                    viewing_date=timezone.now() - timedelta(days=random.randint(1, 30)),
                    status=random.choice(viewing_statuses),
                    feedback=random.choice([
                        'Loved the property, very interested.',
                        'Good property but needs some renovations.',
                        'Price seems high for the area.',
                        'Perfect match for their needs.',
                        'Will discuss with partner and get back.',
                        'Liked the location but wants to see more options.',
                        'Not the right fit, looking for something bigger.',
                        'Very impressed, wants to make an offer.'
                    ]),
                    notes=fake.sentence(nb_words=10),
                )
                viewings.append(viewing)

            # 0-2 offers per property
            for _ in range(random.randint(0, 2)):
                base = float(prop.price) if prop.price else 300000
                offer = PropertyOffer.objects.create(
                    related_property=prop,
                    agent=random.choice(users),
                    buyer_name=fake.name(),
                    buyer_email=fake.email(),
                    buyer_phone=fake.phone_number(),
                    offer_amount=Decimal(str(round(base * random.uniform(0.9, 1.1), -3))),
                    closing_date=future_date(),
                    status=random.choice(offer_statuses),
                    notes=random.choice([
                        'Inspection contingency', 'Financing contingency',
                        'Home sale contingency', 'Appraisal contingency',
                        'None - cash offer', 'Inspection and financing contingencies'
                    ]),
                )
                offers.append(offer)

            # 1-2 notes per property
            for _ in range(random.randint(1, 2)):
                note = PropertyNote.objects.create(
                    related_property=prop,
                    created_by=random.choice(users),
                    content=random.choice(note_contents),
                )
                notes.append(note)

        self.stdout.write(f'  Created {len(units)} units, {len(viewings)} viewings, {len(offers)} offers, {len(notes)} property notes')
