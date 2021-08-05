from django.contrib import admin
from mon.models import TestMongo

# Register your models here.


class TestMonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


admin.site.register(TestMongo, TestMonAdmin)
