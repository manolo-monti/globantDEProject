from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Department, Job, Employee
from .serializers import DepartmentSerializer, JobSerializer, EmployeeSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

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