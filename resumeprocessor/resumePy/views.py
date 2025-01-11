from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Candidate
from .serializers import ItemSerializer
from .forms import ResumeForm


# Create your views here.

def upload(request):
    if request.method == "POST":
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False) # Create instance but don't save to the database yet
            resume.name = "Default Name"  # Replace with dynamic data
            resume.email = "example@example.com"  # Replace with dynamic data
            resume.phone = "1234567890"  # Replace with dynamic data
            resume.save()  # Save to the database

            return render(request, "index.html")
        else:
            print(form.errors)
        # name = "default name"
        # email = "default@mail.com"
        # phone = "+91 99988"
        # Resume.save(name=name, email=email, phone=phone)
        return render(request, "index.html")

    return render(request, "index.html")
# @api_view(['GET'])
# def index(request):
#     items = Resume.objects.all()
#     serializer = ItemSerializer(items, many=True)
#     detail = {'name':'farzeen', 'age':'19'}
#     return Response(serializer.data)
#     # return render(request, "index.html")

@api_view(['POST'])
def index(request):
    # items = Resume.objects.all()
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
    # return render(request, "index.html")
