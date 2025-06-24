from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import SignupSerializer, LoginSerializer,LogoutSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer,WebhookEventSerializer,NumberInputSerializer,ResultSerializer
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from .models import Profile
from django.db import transaction
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .tasks import send_welcome_email
from multiprocessing import Process, Queue
import threading
from rest_framework.views import APIView
from .models import Number


# CPU-bound function for multiprocessing
def square_cpu(number, q):
    q.put({'original': number, 'result': number * number})

# IO-bound simulation for multithreading
def square_io(number, results):
    results.append({'original': number, 'result': number * number})

class SquareNumberAPI(APIView):
    def post(self, request, *args, **kwargs):
        serializer = NumberInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        numbers = serializer.validated_data['numbers']
        mode = request.query_params.get('mode', 'thread')

        result_data = []
        if mode == 'process':
            processes = []
            q = Queue()
            for num in numbers:
                p = Process(target=square_cpu, args=(num, q))
                processes.append(p)
                p.start()

            for p in processes:
                p.join()

            while not q.empty():
                result_data.append(q.get())
        else:
            # MULTITHREADING
            threads = []
            results = []
            for num in numbers:
                t = threading.Thread(target=square_io, args=(num, results))
                threads.append(t)
                t.start()

            for t in threads:
                t.join()

            result_data = results

        return Response(ResultSerializer(result_data, many=True).data)


User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user_email = "akshitachotaliya3@gmail.com"
        send_welcome_email.delay(user_email)
        return Response({"message": "User created !! Email will be sent shortly.", "user_id": user.id}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    print("<--- serializer --->",serializer)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    token = request.auth
    print("<--- token --->",token)
    if token:
        token.delete()
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
    return Response({'error': 'Token not found or already deleted'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def password_reset_request(request):
    serializer = PasswordResetRequestSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.get(email=serializer.validated_data['email'])

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        return Response({
            'message': 'Password reset link generated',
            'uid': uid,
            'token': token
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def password_reset_confirm(request):
    serializer = PasswordResetConfirmSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Password has been reset successfully'}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def webhook_listener(request):
    serializer = WebhookEventSerializer(data=request.data)
    if serializer.is_valid():
        webhook_event = serializer.save()
        return Response({'message': 'Webhook event received', 'event_id': webhook_event.reference_id}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@transaction.atomic
def register_user(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        Profile.objects.create(user=user)
        return Response({"message": "User and profile created", "user_id": user.id}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)