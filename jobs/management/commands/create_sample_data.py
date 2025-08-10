# jobs/management/commands/create_sample_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from companies.models import Company
from jobs.models import Job, Category
from applications.models import Application
import random
from datetime import datetime, timedelta
from faker import Faker 
from django.utils import timezone

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Create sample data for the job board'

    def add_arguments(self, parser):
        parser.add_argument(
            '--companies',
            type=int,
            default=10,
            help='Number of companies to create'
        )
        parser.add_argument(
            '--jobs',
            type=int,
            default=50,
            help='Number of jobs to create'
        )
        parser.add_argument(
            '--job_seekers',
            type=int,
            default=20, # Number of job seekers to create
            help='Number of job seekers to create'
        )
        parser.add_argument(
            '--applications_per_job_seeker',
            type=int,
            default=3, # Average applications per job seeker
            help='Average number of applications each job seeker will submit'
        )


    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting sample data creation...'))

        # --- 1. Create Categories ---
        categories_data = [
            {'name': 'Software Development', 'icon': 'fas fa-code'},
            {'name': 'Data Science', 'icon': 'fas fa-chart-bar'},
            {'name': 'Design', 'icon': 'fas fa-paint-brush'},
            {'name': 'Marketing', 'icon': 'fas fa-bullhorn'},
            {'name': 'Sales', 'icon': 'fas fa-handshake'},
            {'name': 'Customer Support', 'icon': 'fas fa-headset'},
            {'name': 'Human Resources', 'icon': 'fas fa-users'},
            {'name': 'Finance', 'icon': 'fas fa-dollar-sign'},
            {'name': 'Operations', 'icon': 'fas fa-cogs'},
            {'name': 'Product Management', 'icon': 'fas fa-tasks'},
            {'name': 'Healthcare', 'icon': 'fas fa-hand-holding-medical'},
            {'name': 'Education', 'icon': 'fas fa-graduation-cap'},
            {'name': 'Engineering', 'icon': 'fas fa-hard-hat'},
            {'name': 'Art & Culture', 'icon': 'fas fa-palette'},
            {'name': 'Hospitality', 'icon': 'fas fa-utensils'},
        ]
        
        categories = []
        self.stdout.write('Creating categories...')
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': slugify(cat_data['name']),
                    'icon': cat_data['icon'],
                    'description': f'{cat_data["name"]} related positions'
                }
            )
            categories.append(category)
            if created:
                self.stdout.write(f'  Created category: {category.name}')
        self.stdout.write(self.style.SUCCESS(f'Created {len(categories)} categories.'))

        # --- 2. Create Employer User ---
        self.stdout.write('Creating employer user...')
        employer_user, created = User.objects.get_or_create(
            username='employer_demo',
            defaults={
                'email': 'employer@example.com',
                'first_name': 'Demo',
                'last_name': 'Employer',
                'role': 'employer',
                'is_staff': True,
                'is_active': True,
            }
        )
        if created:
            employer_user.set_password('employer123') 
            employer_user.save()
            self.stdout.write(self.style.SUCCESS(f'Created employer user: {employer_user.username}'))
        else:
            self.stdout.write(f'Employer user "{employer_user.username}" already exists.')

        # --- 3. Create Sample Companies ---
        self.stdout.write('Creating companies...')
        companies = []
        unique_company_names = set()
        while len(companies) < options['companies']:
            company_name = fake.company()
            if company_name not in unique_company_names:
                unique_company_names.add(company_name)
                company, created = Company.objects.get_or_create(
                    name=company_name,
                    defaults={
                        'slug': slugify(company_name),
                        'description': fake.paragraph(nb_sentences=5),
                        'location': fake.city() + ', ' + fake.state_abbr(),
                        'size': random.choice(['1-10', '11-50', '51-200', '201-500', '1000+']),
                        'industry': random.choice([
                            'Technology', 'Healthcare', 'Finance', 'E-commerce',
                            'Education', 'Media', 'Gaming', 'Consulting',
                            'Manufacturing', 'Retail', 'Telecommunications', 'Automotive'
                        ]),
                        'founded_year': random.randint(1980, 2023),
                        'website': fake.url(),
                        'is_verified': random.choice([True, False]),
                        'email': fake.company_email(),
                        'linkedin_url': f'https://linkedin.com/company/{slugify(company_name)}',
                        'twitter_url': f'https://twitter.com/{slugify(company_name)}'
                    }
                )
                companies.append(company)
                if created:
                    self.stdout.write(f'  Created company: {company.name}')
                else:
                    self.stdout.write(f'  Company "{company.name}" already exists, skipping.')
        self.stdout.write(self.style.SUCCESS(f'Created {len(companies)} companies.'))

        # --- 4. Create Job Seeker Users ---
        self.stdout.write('Creating job seeker users...')
        job_seekers = []
        for i in range(options['job_seekers']):
            username = f'jobseeker_{i+1}'
            email = f'{username}@example.com'
            job_seeker, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': fake.first_name(),
                    'last_name': fake.last_name(),
                    'role': 'user', # Role for job seekers
                    'is_active': True,
                }
            )
            if created:
                job_seeker.set_password('jobseeker123') # Set a default password
                job_seeker.save()
                self.stdout.write(f'  Created job seeker: {job_seeker.username}')
            job_seekers.append(job_seeker)
        self.stdout.write(self.style.SUCCESS(f'Created {len(job_seekers)} job seekers.'))


        # --- 5. Create Jobs ---
        self.stdout.write('Creating jobs...')
        job_titles = [
            'Software Engineer', 'Data Scientist', 'UX Designer', 'Marketing Manager',
            'Sales Representative', 'Customer Support Specialist', 'HR Generalist',
            'Financial Analyst', 'Operations Manager', 'Product Manager',
            'Backend Developer', 'Frontend Developer', 'Fullstack Developer',
            'DevOps Engineer', 'Cloud Engineer', 'AI/ML Engineer', 'Business Analyst',
            'Project Manager', 'Technical Writer', 'QA Engineer', 'Mobile Developer'
        ]
        
        jobs = []
        for i in range(options['jobs']):
            title = random.choice(job_titles)
            company = random.choice(companies)
            category = random.choice(categories)
            is_remote = random.choice([True, False, False]) # More chance of non-remote
            remote_type = random.choice(['full_remote', 'hybrid']) if is_remote else ''
            location = 'Remote' if is_remote else fake.city() + ', ' + fake.state_abbr()
            
            salary_min = random.randint(40000, 150000)
            salary_max = salary_min + random.randint(10000, 50000)
            
            job_type = random.choice(['full_time', 'part_time', 'contract', 'internship'])
            experience_level = random.choice(['entry_level', 'junior', 'mid_level', 'senior', 'lead'])
            
            expires_at = datetime.now() + timedelta(days=random.randint(1, 60))

            job, created = Job.objects.get_or_create(
                title=title,
                company=company,
                category=category,
                posted_by=employer_user, # All jobs posted by the demo employer
                defaults={
                    'slug': slugify(f"{company.name}-{title}-{i}-{random.randint(1000,9999)}"), # Ensure unique slug
                    'description': fake.paragraphs(nb=3, ext_word_list=None),
                    'requirements': fake.paragraphs(nb=2, ext_word_list=None),
                    'responsibilities': fake.paragraphs(nb=2, ext_word_list=None),
                    'benefits': fake.paragraphs(nb=1, ext_word_list=None),
                    'job_type': job_type,
                    'experience_level': experience_level,
                    'skills_required': fake.sentence(nb_words=10),
                    'location': location,
                    'is_remote': is_remote,
                    'remote_type': remote_type,
                    'salary_min': salary_min,
                    'salary_max': salary_max,
                    'salary_currency': 'USD',
                    'salary_type': random.choice(['annual', 'hourly']),
                    'show_salary': random.choice([True, False]),
                    'accept_applications': True,
                    'application_url': fake.url() if random.random() < 0.5 else '',
                    'application_email': fake.email() if random.random() < 0.5 else '',
                    'status': random.choice(['active', 'paused']),
                    'is_active': True,
                    'is_featured': random.choice([True, False, False]), # Less likely to be featured
                    'is_urgent': random.choice([True, False, False]), # Less likely to be urgent
                    'expires_at': expires_at,
                    'views_count': random.randint(10, 500),
                }
            )
            jobs.append(job)
            if created:
                self.stdout.write(f'  Created job: {job.title} at {job.company.name}')
        self.stdout.write(self.style.SUCCESS(f'Created {len(jobs)} jobs.'))

        # --- 6. Create Applications ---
        self.stdout.write('Creating applications...')
        applications_created_count = 0
        for job_seeker in job_seekers:
            num_applications = random.randint(1, options['applications_per_job_seeker'] * 2) # Vary applications per seeker
            applied_jobs = set()
            for _ in range(num_applications):
                if not jobs: 
                    break
                
                job = random.choice(jobs)
                # Ensure unique application for this job seeker and job
                if job.id in applied_jobs:
                    continue
                
                applied_jobs.add(job.id)

                status = random.choice([
                    'pending', 'reviewed', 'shortlisted', 'interviewed',
                    'rejected', 'accepted', 'withdrawn'
                ])
                
                applied_at_naive = fake.date_time_between(start_date="-3m", end_date="now")
                
                # Make it timezone-aware ONLY IF it's naive
                if timezone.is_naive(applied_at_naive):
                    applied_at = timezone.make_aware(applied_at_naive)
                else:
                    applied_at = applied_at_naive # It's already aware
                
                # Calculate updated_at based on the potentially aware applied_at
                updated_at_naive = applied_at_naive + timedelta(days=random.randint(0, 30)) if status != 'pending' else applied_at_naive

                if timezone.is_naive(updated_at_naive):
                    updated_at = timezone.make_aware(updated_at_naive)
                else:
                    updated_at = updated_at_naive # It's already aware

                reviewed_at = None
                if status in ['reviewed', 'shortlisted', 'interviewed', 'rejected', 'accepted']:
                    reviewed_at_naive = updated_at_naive # Use the naive version to potentially make it aware
                    if timezone.is_naive(reviewed_at_naive):
                        reviewed_at = timezone.make_aware(reviewed_at_naive)
                    else:
                        reviewed_at = reviewed_at_naive # Already aware

                application, created = Application.objects.get_or_create(
                    job=job,
                    applicant=job_seeker,
                    defaults={
                        'cover_letter': fake.paragraph(nb_sentences=4),
                        'resume_url': fake.url() + '/resume.pdf',
                        'portfolio_url': fake.url() if random.random() < 0.5 else '',
                        'linkedin_url': fake.url() if random.random() < 0.7 else '',
                        'phone': fake.phone_number(), # Max length was increased to 50
                        'email': job_seeker.email,
                        'status': status,
                        'admin_notes': fake.paragraph(nb_sentences=2) if random.random() < 0.3 else '',
                        'rejection_reason': fake.sentence() if status == 'rejected' else '',
                        'applied_at': applied_at, # Use the aware datetime
                        'updated_at': updated_at, # Use the aware datetime
                        'reviewed_at': reviewed_at, # Use the aware or None datetime
                        'years_of_experience': random.randint(0, 10),
                        'expected_salary': random.randint(30000, 120000),
                        'availability_date': fake.date_between(start_date="today", end_date="+6m") if random.random() < 0.7 else None,
                    }
                )
                if created:
                    applications_created_count += 1
                    # self.stdout.write(f'  Created application for {job_seeker.username} to {job.title}') # Too verbose for many apps
        self.stdout.write(self.style.SUCCESS(f'Created {applications_created_count} applications.'))
        self.stdout.write(self.style.SUCCESS('Sample data creation complete!'))