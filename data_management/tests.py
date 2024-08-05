from django.test import TestCase

# Create your tests here.
from rest_framework import status
from rest_framework.test import APIClient
from .models import Department, Job, Employee

class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create some test data
        self.department = Department.objects.create(id=1, department='HR')
        self.job = Job.objects.create(id=1, job='Manager')
        self.employee = Employee.objects.create(id=1, name='John Doe', datetime='2021-01-01T00:00:00Z', department=self.department, job=self.job)

    def test_get_departments(self):
        response = self.client.get('/api/departments/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_jobs(self):
        response = self.client.get('/api/jobs/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_employees(self):
        response = self.client.get('/api/employees/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_successful_bulk_insert(self):
        data = [
            {'id': 2, 'name': 'Manu Doe', 'datetime': '2021-08-05T00:00:00Z', 'department_id': 1, 'job_id': 1},
            {'id': 3, 'name': 'Jane Doe', 'datetime': '2021-05-05T00:00:00Z', 'department_id': 1, 'job_id': 1},
        ]
        response = self.client.post('/api/employees/bulk_insert/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'status': 'Batch insert successful'})
        self.assertEqual(Employee.objects.count(), 3)

    def test_invalid_data_format(self):
        data = {'name': 'John Doe', 'datetime': '2021-08-05T00:00:00Z', 'department_id': 1, 'job_id': 1}
        response = self.client.post('/api/employees/bulk_insert/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Expected a list of employee data'})
        self.assertEqual(Employee.objects.count(), 1)

    def test_batch_size_exceeded(self):
        data = []
        for i in range(1001):  # Exceed limit of 1000
            data.append({"id": i, "name": f"Employee {i}", 'datetime': '2021-01-01T00:00:00Z', 'department_id': 1, 'job_id': 1})
        response = self.client.post('/api/employees/bulk_insert/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Batch size exceeds 1000'})
        self.assertEqual(Employee.objects.count(), 1)

    def test_missing_field(self):
        data = [
            {'name': 'John Doe', 'datetime': '2024-08-05T00:00:00Z', 'department_id': 1},
            {'id': 2, 'datetime': '2024-08-05T00:00:00Z', 'job_id': 2},
        ]
        response = self.client.post('/api/employees/bulk_insert/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': "Missing field 'id'"})
        self.assertEqual(Employee.objects.count(), 1)
