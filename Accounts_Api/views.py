from django.shortcuts import render
from rest_framework import generics
from .serializers import UserRegisterSerializer
from rest_framework.response import Response
# Create your views here.


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.save()
        return Response({
            'user':UserRegisterSerializer(user,context = self.get_serializer_context()).data,
            'message':"Registration Successful. Now perform login to get your token.",
        })