from django.shortcuts import render
from rest_framework import generics
from django.contrib.sites.shortcuts import get_current_site

from .models import Account
from .serializers import UserRegisterSerializer
from rest_framework.response import Response
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.urls import reverse
# Create your views here.


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    def post(self,request,*args,**kwargs):
        user = request.data
        serializer = self.get_serializer(data = user)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        user_data = serializer.data
        
        user = Account.objects.get(email = user_data['email'])
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+default_token_generator.make_token(user)
        email_body = 'Hi  '+ user.first_name +',\n' + "Please click on below link to confirm your registration. \n"+ absurl + '\n If you think its not you, please ignore this email.'
        
        data = {'email_body':email_body,'to_email':user.email,'mail_subject':'Please activate your account'}
        Util.send_email(data)

        return Response({
            'user':UserRegisterSerializer(user,context = self.get_serializer_context()).data,
            'message':"Registration Successful. Now perform login to get your token.",
        })
        
        
        
class VerifyEmail(generics.GenericAPIView):
    def get(self):
        pass
