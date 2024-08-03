import pandas as pd
from django.core.management.base import BaseCommand
from data_management.models import Department, Job, Employee

class Command(BaseCommand):
    help = 'Load data from CSV files'

    def handle(self, *args, **kwargs):
        try:
            departments = pd.read_csv('csv_files/departments.csv', names=['id', 'department'], header=None)
            jobs = pd.read_csv('csv_files/jobs.csv', names=['id', 'job'], header=None)
            employees = pd.read_csv('csv_files/hired_employees.csv', names=['id', 'name', 'datetime', 'department_id', 'job_id'], header=None)

            for _, row in departments.iterrows():
                if pd.notnull(row['id']) and pd.notnull(row['department']):
                    Department.objects.create(id=row['id'], department=row['department'])

            for _, row in jobs.iterrows():
                if pd.notnull(row['id']) and pd.notnull(row['job']):
                    Job.objects.create(id=row['id'], job=row['job'])

            for _, row in employees.iterrows():
                if pd.notnull(row['id']) and pd.notnull(row['name']) and pd.notnull(row['datetime']) and pd.notnull(row['department_id']) and pd.notnull(row['job_id']):
                    Employee.objects.create(
                        id=row['id'], name=row['name'], datetime=row['datetime'],
                        department_id=row['department_id'], job_id=row['job_id']
                    )
        except Exception as e:
            self.stderr.write(f"Error loading data: {e}")
