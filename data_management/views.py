from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Department, Job, Employee
from .serializers import DepartmentSerializer, JobSerializer, EmployeeSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
import pandas as pd

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    @action(detail=False, methods=['post'])
    def bulk_insert(self, request):
        data = request.data
        if not isinstance(data, list):
            return Response({"error": "Expected a list of employee data"}, status=status.HTTP_400_BAD_REQUEST)

        if len(data) > 1000:
            return Response({"error": "Batch size exceeds 1000"}, status=status.HTTP_400_BAD_REQUEST)

        employees = []
        for item in data:
            try:
                employee = Employee(
                    id=item['id'],
                    name=item['name'],
                    datetime=item['datetime'],
                    department_id=item['department_id'],
                    job_id=item['job_id']
                )
                employees.append(employee)
            except KeyError as e:
                return Response({"error": f"Missing field {e}"}, status=status.HTTP_400_BAD_REQUEST)

        Employee.objects.bulk_create(employees)
        return Response({"status": "Batch insert successful"}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def hires_by_quarter(self, request):
        employees = Employee.objects.filter(datetime__year=2021)
        df = pd.DataFrame(employees.values('department__department', 'job__job', 'datetime'))
        df['quarter'] = df['datetime'].dt.quarter
        
        # Group by department, job, and quarter, count employees if no data default = 0
        result = df.groupby(['department__department', 'job__job', 'quarter']).size().unstack(fill_value=0)
        
        # columns name change from 1 to 4, to q1 to q4
        result.columns = ['q1', 'q2', 'q3', 'q4']

        # Order by department, job
        result = result.reset_index().sort_values(['department__department', 'job__job'])

        return Response(result.to_dict('records'))
    
    @action(detail=False, methods=['get'])
    def above_mean_hires(self, request):
        employees = Employee.objects.filter(datetime__year=2021)
        df = pd.DataFrame(list(employees.values('department__id', 'department__department', 'name')))
        
        # Count employees by department
        hires_per_department = df.groupby(['department__id', 'department__department']).size().reset_index(name='hires')
        
        # Mean of count employees by department
        mean_hires = hires_per_department['hires'].mean()
        
        # Departments with count of employees over mean ordered by count of employees desc
        result = hires_per_department[hires_per_department['hires'] > mean_hires].sort_values(by='hires', ascending=False)

        return Response(result.to_dict(orient='records'))