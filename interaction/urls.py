from interaction.views import GetReport
from django.urls import path
urlpatterns = [path('report', GetReport.as_view(),
                    name='get inter actions of users')]
