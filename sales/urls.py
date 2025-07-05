from django.urls import path
from .views import getCustomers,upload_csv,refresh_data,total_revenue,revenue_by_category,revenue_by_product,revenue_by_region


urlpatterns = [
    path('upload/', upload_csv, name='upload_csv'),
    path('refresh-data/', refresh_data, name='refresh_data'),
    path('analytics/revenue/total/', total_revenue),
    path('analytics/revenue/by-category/', revenue_by_category, name='revenue_by_category'),
    path('analytics/revenue/by-product/', revenue_by_product),
    path('analytics/revenue/by-region/', revenue_by_region),
    path('get-customers/', getCustomers, name='getCustomers')
]