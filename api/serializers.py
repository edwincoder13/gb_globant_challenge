from rest_framework import serializers
from .models import departments
from .models import jobs
from .models import hired_employees

class departments_serializer(serializers.ModelSerializer):
    class Meta:
        model = departments
        fields = '__all__'

class jobs_serializer(serializers.ModelSerializer):
    class Meta:
        model = jobs
        fields = '__all__'

class hired_employees_serializer(serializers.ModelSerializer):
    class Meta:
        model = hired_employees
        fields = '__all__'