import os
import django
from fastapi import FastAPI

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from sales.fastapi_routes.api import router as sales_router

app = FastAPI()

app.include_router(sales_router, prefix="/fastapi")
