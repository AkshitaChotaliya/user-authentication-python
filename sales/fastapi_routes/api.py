
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from fastapi import APIRouter
from sales.models import Customer

router = APIRouter()

@router.get("/customers")
def get_customers():
    return [{"id": c.customer_id, "name": c.name} for c in Customer.objects.all()]