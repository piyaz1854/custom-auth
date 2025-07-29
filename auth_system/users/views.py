import bcrypt
import jwt
import os
from datetime import datetime
from dotenv import load_dotenv

from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django import forms
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer
from .permissions import has_permission

# site:
def home_page(request):
    content = {
        'title':'UserForge',
        'year': datetime.now().year
    }
    return render(request, 'customuser/home_page.html', content)

def privacy(request):
    content = {
        'title':'UserForge',
        'year': datetime.now().year
    }
    return render(request, 'customuser/privacy.html', content)

def contact(request):
    content = {
        'title':'UserForge',
        'year': datetime.now().year
    }
    return render(request, 'customuser/contact.html', content)


# api:
class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput, label="verify password"
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password2'):
            raise forms.ValidationError("passwords doesn't match")
        return cleaned_data

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.create_user(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            request.session['user_id'] = user.id
            return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'customuser/register.html', {
        'title': 'register',
        'form': form,
        'year': datetime.now().year
    })

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(email=email)

            if not user.is_active:
                return render(
                    request, 'customuser/login.html',
                    {'error': 'account is not active'}
                )

            if bcrypt.checkpw(password.encode(), user.password.encode()):
                request.session['user_id'] = user.id 
                request.session['user_email'] = user.email 
                return redirect('/')
            else:
                return render(
                    request, 'customuser/login.html',
                    {'error': 'password is not correct'}
                )
        except CustomUser.DoesNotExist:
            return render(
                request, 'customuser/login.html',
                {'error': 'user not found'})

    return render(request, 'customuser/login.html')

def logout_view(request):
    request.session.flush()
    return redirect('/')


@login_required
def delete_account_view(request):
    if request.method == 'POST':
        user = request.user
        user.is_active = False
        user.save()
        response = redirect('home')
        return response

    return render(request)


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "user registered"},
                status=201
            )
        return Response(serializer.errors, status=400)

    def get(self, request):
        return Response({
        "message": "send POST to register"
    })

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            payload = {"user_id": user.id}
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
            return Response({"token": token})
        return Response(serializer.errors, status=400)

    def get(self, request):
        return Response({
        "message": "send POST to login"
    })

class LogoutView(APIView):
    def post(self, request):
        return Response({"message": "user logout of system"}, status=200)

class ProfileView(APIView):
    def get(self, request):
        user = request.user

        if user is None or not user.is_authenticated:
            return Response({"detail": "unauthorized"}, status=401)

        if not has_permission(user, 'read', 'user', is_owner=True):
            return Response({"detail": "Forbidden"}, status=403)

        return Response({
            "user_id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role.name if user.role else None,
        })

class DeleteAccountView(APIView):
    def delete(self, request):

        user = request.user
        if user is None or not user.is_authenticated:
            return Response({"detail": "Unauthorized"}, status=401)

        user.is_active = False
        user.save()
        return Response({"message": "account deleted"}, status=200)
