from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings  # Add this import for settings

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt  
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    # Validate input
    if not username or not password:
        return Response({
            'error': 'Please provide both username and password'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            response = Response({
                'token': token.key,
                'username': user.username,
                'user_id': user.pk,
                'success': True
            })
            
            # Add CORS headers
            response["Access-Control-Allow-Origin"] = "http://localhost:3000"
            response["Access-Control-Allow-Credentials"] = "true"
            response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
            response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
            
            return response
            
        return Response(
            {
                'error': 'Invalid credentials',
                'success': False
            }, 
            status=status.HTTP_401_UNAUTHORIZED
        )
    except Exception as e:
        print(f"Login error: {str(e)}")
        return Response(
            {
                'error': 'An error occurred during login',
                'success': False,
                'detail': str(e) if settings.DEBUG else None
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST', 'OPTIONS'])
@csrf_exempt
def logout_view(request):
    if request.method == 'OPTIONS':
        response = Response()
        response["Access-Control-Allow-Origin"] = "http://localhost:3000"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response
        
    if request.user.is_authenticated:
        try:
            Token.objects.filter(user=request.user).delete()
            response = Response({
                'message': 'Successfully logged out',
                'success': True
            })
            
            # Add CORS headers
            response["Access-Control-Allow-Origin"] = "http://localhost:3000"
            response["Access-Control-Allow-Credentials"] = "true"
            
            return response
        except Exception as e:
            print(f"Logout error: {str(e)}")
            return Response(
                {
                    'error': 'Error during logout',
                    'success': False
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    return Response(
        {
            'error': 'Not logged in',
            'success': False
        }, 
        status=status.HTTP_401_UNAUTHORIZED
    )

@api_view(['OPTIONS'])
@permission_classes([AllowAny])
@csrf_exempt
def auth_options(request):
    response = Response()
    response["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response