from django.http import HttpResponse


def home(request):
	return HttpResponse("Root app home page")
