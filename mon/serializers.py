from django.db.models import fields
from mon.models import TestMongo
from django.db import models
from rest_framework import serializers

class TestMonSerializers(serializers.ModelSerializer):
    class Meta:
        model=TestMongo
        fields='__all__'
        
