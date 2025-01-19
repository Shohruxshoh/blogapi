from django.shortcuts import render, get_object_or_404
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import RegisterSerializer, ProfileSerializer
from .models import User, Profile
from drf_spectacular.utils import extend_schema
# Create your views here.

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    serializers_class = ProfileSerializer

    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        serializer = self.serializers_class(profile)
        return Response(serializer.data)

    @extend_schema(
        request=ProfileSerializer,
        responses={200: ProfileSerializer},
        description="Update the profile of the authenticated user"
    )
    def patch(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        serializer = self.serializers_class(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
