from rest_framework import serializers
from base.models import User


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class registrationSerializer(serializers.ModelSerializer):
    # password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = '__all__'
        def save(self):
          user = User(
            email=self.validated_data['email'],
            name=self.validated_data['name'],
            address = self.validated_data['address'],
            given_name=self.validated_data['given_name'],
            family_name=self.validated_data['family_name'],
            username= self.valdiated_data['name']

            
        )
          user.save()
          return user

# class updateUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['first_name','last_name','address','phone','age','work','profile_picture','cover_picture']
#     def save(self):
#         first_name=self.validated_data['first_name']
#         last_name=self.validated_data['last_name']
#         phone  = self.validated_data['phone']
#         address = self.validated_data['address']
#         age = self.validated_data['age']
#         work = self.validated_data['work']
#         profile_pic = self.validated_data['profile_pic']
#         cover_pic = self.validated_data['cover_pic']
#         if(first_name is not null):
#             user.first_name = first_name
#         if(last_name is not null):
#             user.last_name = last_name
#         if(Nationality is not null):
#             user.address = address
#         if(phone is not null):
#             user.phone = phone
#         if(profile_pic is not null):
#             user.profile_picture = profile_pic
#         if(profile_pic is not null):
#             user.profile_picture = profile_pic
#         if(age is not null):
#             user.age = age
#         if(work is not null):
#             user.work = work
#         user.save()    

