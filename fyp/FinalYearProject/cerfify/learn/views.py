from django.shortcuts import render
from .models import Learnm


# Create your views here.
def home(request):
	context={
		'posts':Learnm.objects.all()
	}
	return render(request, 'learn/home.html',context)


