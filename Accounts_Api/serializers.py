
from rest_framework import fields, serializers
from .models import Account
import re

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style = {'input_type':'password'},write_only = True)
    class Meta:
        model = Account
        fields = ['first_name','last_name','username','email','phone_number','password','password2']
        extra_kwargs = {
            'password':{'write_only':True}
        }
        
    
    def save(self):
        register = Account(
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name'],
            username = self.validated_data['username'],
            email = self.validated_data['email'],
            phone_number = self.validated_data['phone_number'],
        )
        if Account.objects.filter(phone_number = self.validated_data['phone_number']).exists():
            raise serializers.ValidationError({'error':'This Phone Number Already Registered.!'})
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2 :
            raise serializers.ValidationError({'error':'Password Does Not Match.!'})
        if password:
            reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
            
            # compiling regex
            pattern = re.compile(reg)

            # searching regex                 
            match = re.search(pattern, password)

            # validating conditions
            if match == None:
                raise serializers.ValidationError({
                    "errors":"Password should contain Uppercase, Lowercase, Numeric and Special Characters."
                })
        register.set_password(password)
        register.is_active = False
        register.save()
        return register
        
        