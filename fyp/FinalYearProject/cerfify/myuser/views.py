from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import authenticate, login
from .models import MyUser
from  django.contrib.auth import get_user_model
from  django.contrib.auth.models import User
from projects.models import Project


class RegistrationForm(UserCreationForm) :
    email = forms.EmailField(required=True)

    class Meta :
        model = MyUser
        fields = (
        'username',
        'first_name',
        'last_name',
        'email',
        'date_of_birth',
        'password1',
        'password2',
        )

    def save(self,commit=True) :
        user = super(RegistrationForm,self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.date_of_birth = self.cleaned_data['date_of_birth']

        if commit :
            user.save()
            return user


def register(request) :
    if request.method == "POST" :
        form = RegistrationForm(request.POST)
        if form.is_valid() :
            user=form.save()
            #user= authenticate(username = username, password = password)
            login(request,user)
            return redirect("projects:feed")
            #return HttpResponseRedirect(reverse("projects:feed",))

    else :
        form = RegistrationForm()

    context = { 'form':form}
    return render(request,'my/register.html',context)

def profile(request) :
    User = get_user_model()
    user =  User.objects.get(username=request.user)
    myprojects = Project.objects.filter(creator=str(request.user))
    context = { 'user':user,'projects':myprojects}
    context['percentage'] = user.score * 100/ user.get_threshold()
    return render(request,'my/profile.html',context)

