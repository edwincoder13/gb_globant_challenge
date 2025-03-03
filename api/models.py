from django.db import models

class departments(models.Model):
    id_departments = models.IntegerField(primary_key=True)
    name_departments = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class jobs(models.Model):
    id_jobs = models.IntegerField(primary_key=True)
    name_jobs = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
    
class hired_employees(models.Model):
    id_employ = models.IntegerField(primary_key=True)
    name_employ = models.CharField(max_length=200)
    datetime = models.CharField(max_length=200)
    department_id = models.IntegerField()
    job_id = models.IntegerField()
    
    def __str__(self):
        return self.nombre