from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from .serializers import RegisterSerializer, LoginSerializer, AdminCreateSerializer


def get_tokens(user):

    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }


class RegisterView(APIView):
    @extend_schema(request=RegisterSerializer, responses={201: RegisterSerializer})
    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():

            user = serializer.save()

            return Response({
                "message": "User created",
                "tokens": get_tokens(user)
            })

        return Response(serializer.errors, status=400)
    
class LoginView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(request=LoginSerializer,auth=[], responses={200: {"tokens": {"refresh": "string", "access": "string"}}})
    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():

            user = serializer.validated_data

            return Response({
                "tokens": get_tokens(user)
            })

        return Response(serializer.errors, status=400)
    
class CreateAdminView(APIView):

    permission_classes = [IsAuthenticated]
    @extend_schema(request=AdminCreateSerializer, responses={201: AdminCreateSerializer})
    def post(self, request):

        if request.user.role != "ADMIN":
            return Response({"error": "Only admin allowed"}, status=403)

        serializer = AdminCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)