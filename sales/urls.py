from django.urls import path
from .views import getCustomers,upload_csv,refresh_data


urlpatterns = [
    path('upload/', upload_csv, name='upload_csv'),
    path('refresh-data/', refresh_data, name='refresh_data'),
    path('get-customers/', getCustomers, name='getCustomers')
]