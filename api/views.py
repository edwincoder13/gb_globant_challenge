import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from rest_framework import viewsets
from .models import departments
from .serializers import departments_serializer
from .models import jobs
from .serializers import jobs_serializer
from .models import hired_employees
from .serializers import hired_employees_serializer

from django.db import connection

class departments_view_set(viewsets.ModelViewSet):
    queryset = departments.objects.all()
    serializer_class = departments_serializer

class jobs_view_set(viewsets.ModelViewSet):
    queryset = jobs.objects.all()
    serializer_class = jobs_serializer

class hired_employees_view_set(viewsets.ModelViewSet):
    queryset = hired_employees.objects.all()
    serializer_class = hired_employees_serializer

class csv_upload_rds(APIView):
    def post(self, request, format=None):
        batch_size, departments_list, job_list, hired_list = 1000, [], [], []
        file = request.FILES.get('file')
        table_name = request.data.get('table_name')
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        if not table_name:
            return Response({"error": "No table provided"}, status=status.HTTP_400_BAD_REQUEST)
        df = pd.read_csv(file, header=None)
        if table_name == 'departments':
            for _, row in df.iterrows():
                data = departments(id_departments=row[0], name_departments=row[1])
                departments_list.append(data)
            bulk_lotes(departments_list, batch_size, table_name)
        elif table_name == 'jobs':
            for _, row in df.iterrows():
                data = jobs(id_jobs=row[0], name_jobs=row[1])
                job_list.append(data)
            bulk_lotes(job_list, batch_size, table_name)
        elif table_name == 'hired_employees':
            df = fillna_df_columns_zero(df, [3, 4])
            for _, row in df.iterrows():
                data = hired_employees(id_employ=row[0], name_employ=row[1], datetime=row[2], department_id=row[3], job_id=row[4])
                hired_list.append(data)
            bulk_lotes(hired_list, batch_size, table_name)
        else:
            return Response({"error": "Not valid table"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "File uploaded successfully"}, status=status.HTTP_200_OK)

class get_numberofemployees_hired(APIView):
    def get(self, request, format=None):
        query = """SELECT C.name_departments AS deparments,
	                      B.name_jobs AS jobs, 
	                      COUNT(CASE WHEN MONTH(TRY_CONVERT(DATETIME, A.[datetime])) IN (1,2,3) THEN 1 END) AS Q1,
	                      COUNT(CASE WHEN MONTH(TRY_CONVERT(DATETIME, A.[datetime])) IN (4,5,6) THEN 1 END) AS Q2,
	                      COUNT(CASE WHEN MONTH(TRY_CONVERT(DATETIME, A.[datetime])) IN (7,8,9) THEN 1 END) AS Q3,
	                      COUNT(CASE WHEN MONTH(TRY_CONVERT(DATETIME, A.[datetime])) IN (10,11,12) THEN 1 END) AS Q4
                   FROM [db-hire-emp].dbo.api_hired_employees AS A
             INNER JOIN [db-hire-emp].dbo.api_jobs AS B
             ON A.job_id = B.id_jobs
             INNER JOIN [db-hire-emp].dbo.api_departments AS C
             ON A.department_id = C.id_departments
             WHERE YEAR(TRY_CONVERT(DATETIME, A.[datetime])) = 2021
             GROUP BY C.name_departments, B.name_jobs
             ORDER BY C.name_departments, B.name_jobs;"""

        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()

        data = [
            {
                'deparments': row[0],
                'jobs': row[1],
                'Q1': row[2],
                'Q2': row[3],
                'Q3': row[4],
                'Q4': row[5],
            } for row in result
        ]
        return Response(data)

class get_numberofemployees_avg(APIView):
    def get(self, request, format=None):
        query = """SELECT C.id_departments AS id,
	                      C.name_departments AS deparments,
	                      COUNT(A.id_employ) AS number_employees
                   FROM [db-hire-emp].dbo.api_hired_employees AS A
                   INNER JOIN [db-hire-emp].dbo.api_departments AS C
                   ON A.department_id = C.id_departments
                   GROUP BY C.id_departments, C.name_departments
                   HAVING COUNT(A.id_employ) > AVG(CASE WHEN YEAR(TRY_CONVERT(DATETIME, A.[datetime])) = 2021 THEN 1 END)
                   ORDER BY C.id_departments, C.name_departments;"""

        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()

        data = [
            {
                'id': row[0],
                'deparments': row[1],
                'number_employees': row[2],
            } for row in result
        ]
        return Response(data)
    
def bulk_lotes(list_data:list, batch_size:int, v_table:str):
    for i in range(0, len(list_data), batch_size):
        if v_table == 'departments':
            departments.objects.bulk_create(list_data[i:i + batch_size])
        elif v_table == 'jobs':
            jobs.objects.bulk_create(list_data[i:i + batch_size])
        elif v_table == 'hired_employees':
            hired_employees.objects.bulk_create(list_data[i:i + batch_size])
        else:
            return Response({"error": "Not valid table"}, status=status.HTTP_400_BAD_REQUEST)

def fillna_df_columns_zero(df, list_columns:list):
    for i in list_columns:
        df[i] = df[i].fillna(0)
    return df

class batch_insert(APIView):
    def post(self, request, format=None):
        data = request.data
        if not isinstance(data, list):
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

        if len(data) > 1000:
            return Response({"error": "Batch size exceeds limit"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = departments_serializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Batch insert successful"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)