from mon.views import AllTestMon, TestQuery
from django.urls import path

urlpatterns = [path('hello', TestQuery.as_view(), name='test api end point'),
               path('all', AllTestMon.as_view(), name='list all mon test ')]
