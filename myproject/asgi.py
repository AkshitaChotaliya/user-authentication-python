"""
ASGI config for myproject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from sales.fastapi_routes.api import router as sales_router


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

fastapi_app = FastAPI()
fastapi_app.include_router(sales_router, prefix="/fastapi")

from starlette.middleware.wsgi import WSGIMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from django.core.handlers.asgi import ASGIHandler

from fastapi.middleware.wsgi import WSGIMiddleware
from starlette.routing import Mount, Router

from starlette.applications import Starlette
from starlette.routing import Mount

application = Starlette(routes=[
    Mount("/fastapi", app=fastapi_app),
    Mount("/", app=get_asgi_application()),
])

# application = get_asgi_application()
