import pandas as pd
from django.http import JsonResponse
from .models import Customer, Product, Order, OrderItem
from io import TextIOWrapper
from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.db import transaction
from django.db.models import F, ExpressionWrapper, DecimalField, Sum




# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
# @authentication_classes([])
def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('file'):

        csv_file = TextIOWrapper(request.FILES['file'].file, encoding='utf-8')
        df = pd.read_csv(csv_file)
        print("DataFrame Columns:", df.columns)
        created_rows = 0
        for _, row in df.iterrows():
            print("<----- row ----->",row)
            customer, _ = Customer.objects.get_or_create(
            customer_id=row['customer_id'],
            defaults={
                'customer_name': row.get('customer_name', ''),
                'customer_email': row.get('customer_email', ''),
                'customer_address': row.get('customer_address', ''),
                'demographics': row.get('demographics') or None
            }
        )
            product, _ = Product.objects.get_or_create(
                product_id=row['product_id'],
                defaults={
                    'product_name': row['product_name'],
                    'category': row['category'],
                    'description': row.get('description', '')
                }
            )

            order, _ = Order.objects.get_or_create(
                order_id=row['order_id'],
                defaults={
                    'customer': customer,
                    'date_of_sale': pd.to_datetime(row['date_of_sale']),
                    'region': row['region'],
                    'payment_method': row['payment_method'],
                    'shipping_cost': row['shipping_cost'],
                    'discount': row['discount'],
                }
            )

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity_sold=row['quantity_sold'],
                unit_price=row['unit_price']
            )

            created_rows += 1
        return JsonResponse({'status': 'success', 'rows_created': created_rows})

    return JsonResponse({'error': 'Invalid request'}, status=400)

        # csv_file = TextIOWrapper(request.FILES['file'].file, encoding='utf-8')
        # df = pd.read_csv(csv_file, usecols=["Order ID", "Customer ID", "Region"])

        # getHead = df.head(5).to_dict(orient='records')  
        # first_3_values = df.iloc[:3, df.columns.get_loc('Region')].tolist()  

        # print("First 3 Region values:", first_3_values)

        # return JsonResponse({
        #     "message": "CSV processed successfully",
        #     "preview": getHead,
        #     "first_3_regions": first_3_values
        # }, status=200)

    # return JsonResponse({"error": "No file uploaded"}, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_data(request):
    if 'file' not in request.FILES:
        return JsonResponse({"error": "CSV file is required."}, status=400)

    csv_file = TextIOWrapper(request.FILES['file'].file, encoding='utf-8')
    df = pd.read_csv(csv_file)

    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('-', '_')

    inserted, updated = 0, 0

    with transaction.atomic():
        for _, row in df.iterrows():
            customer, _ = Customer.objects.get_or_create(
                customer_id=row['customer_id'],
                defaults={
                    'name': row.get('customer_name', ''),
                    'email': row.get('customer_email', ''),
                    'address': row.get('customer_address', ''),
                    'demographics': row.get('demographics') or None
                }
            )

            product, _ = Product.objects.get_or_create(
                product_id=row['product_id'],
                defaults={
                    'name': row.get('product_name', ''),
                    'category': row.get('category', ''),
                    'description': row.get('product_description') or None
                }
            )

            order_data = {
                'customer': customer,
                'date_of_sale': row['date_of_sale'],
                'region': row['region'],
                'payment_method': row['payment_method'],
                'shipping_cost': row['shipping_cost'],
                'discount': row['discount']
            }

            order, created = Order.objects.update_or_create(
                order_id=row['order_id'],
                defaults=order_data
            )

            OrderItem.objects.update_or_create(
                order=order,
                product=product,
                defaults={
                    'quantity_sold': row['quantity_sold'],
                    'unit_price': row['unit_price']
                }
            )

            if created:
                inserted += 1
            else:
                updated += 1

    return JsonResponse({
        "message": "Data refreshed successfully",
        "orders_inserted": inserted,
        "orders_updated": updated,
        "total_rows": len(df)
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def total_revenue(request):
    start = request.GET.get('start_date')
    end = request.GET.get('end_date')
    items = OrderItem.objects.filter(
        order__date_of_sale__range=[start, end]
    ).annotate(
        revenue=ExpressionWrapper(
            F('quantity_sold') * F('unit_price') * (1 - F('order__discount')),
            output_field=DecimalField()
        )
    )

    total = items.aggregate(total_revenue=Sum('revenue'))['total_revenue'] or 0

    return JsonResponse({'total_revenue': float(total)})

@api_view(['GET'])
@permission_classes([AllowAny])
def revenue_by_category(request):
    start = request.GET.get('start_date')
    end = request.GET.get('end_date')

    if not start or not end:
        return JsonResponse({"error": "Please provide start_date and end_date"}, status=400)
    
    items = OrderItem.objects.filter(
        order__date_of_sale__range=[start, end]
    ).annotate(
        revenue=ExpressionWrapper(
            F('quantity_sold') * F('unit_price') * (1 - F('order__discount')),
            output_field=DecimalField()
        )
    ).values('product__category').annotate(
        total_revenue=Sum('revenue')
    ).order_by('-total_revenue')

    return JsonResponse(list(items), safe=False)

@api_view(['GET'])
def revenue_by_product(request):
    start = request.GET.get('start_date')
    end = request.GET.get('end_date')

    if not start or not end:
        return JsonResponse({"error": "Please provide start_date and end_date"}, status=400)

    items = OrderItem.objects.filter(
        order__date_of_sale__range=[start, end]
    ).annotate(
        revenue=ExpressionWrapper(
            F('quantity_sold') * F('unit_price') * (1 - F('order__discount')),
            output_field=DecimalField()
        )
    ).values('product__product_name').annotate(total_revenue=Sum('revenue')).order_by('-total_revenue')

    return JsonResponse(list(items), safe=False)

@api_view(['GET'])
def revenue_by_region(request):
    start = request.GET.get('start_date')
    end = request.GET.get('end_date')

    if not start or not end:
        return JsonResponse({"error": "Please provide start_date and end_date (YYYY-MM-DD)"}, status=400)

    items = OrderItem.objects.filter(
        order__date_of_sale__range=[start, end]
    ).annotate(
        revenue=ExpressionWrapper(
            F('quantity_sold') * F('unit_price') * (1 - F('order__discount')),
            output_field=DecimalField()
        )
    ).values('order__region').annotate(
        total_revenue=Sum('revenue')
    ).order_by('-total_revenue')

    return JsonResponse(list(items))

@api_view(['GET'])
def top_products(request):
    start = request.GET.get('start_date')
    end = request.GET.get('end_date')
    top_n = int(request.GET.get('limit', 5))

    if not start or not end:
        return JsonResponse({"error": "Please provide start_date and end_date (YYYY-MM-DD)"}, status=400)
    
    top_items = OrderItem.objects.filter(order__date_of_sale__range=[start,end]).values('product__product_name').annotate(total_quantuty=Sum('quantity_sold')).order_by('-total_quantuty')[:top_n]

    return JsonResponse(list(top_items))


@api_view(['GET'])
def getCustomers(request):
    data = [{"name": "test"}]
    return JsonResponse(data, safe=False)