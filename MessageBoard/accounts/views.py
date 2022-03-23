from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from .models import OneTimeCode
from django.contrib.auth.models import User
from random import randint


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            code = OneTimeCode.objects.create(code=randint(1000, 9999), user=user)
            subject = f"Ваш код подтверждения для регистрации на форуме гиков: {code.code}"
            message = f"Ваш код подтверждения для регистрации на форуме гиков: {code.code}"
            user.email_user(subject, message)
            user_id = user.id
            return redirect("confirmation", user_id=user_id)
    form = NewUserForm()
    return render (request=request, template_name="register.html", context={"register_form":form})

def verify_registration(request, user_id):
    if request.method == "POST":
        code = request.POST['code']
        user = User.objects.get(id = user_id)
        if OneTimeCode.objects.filter(code=code, user=user).exists():
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, "Вы зарегистрированы." )
            return redirect("main")
        else:
            messages.error(request, "Код неверный.")
            return redirect("register")
    return render (request=request, template_name="signup_confirmation.html")





