from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Candidate
from .serializers import ItemSerializer
from .forms import ResumeForm
from .utils import parse_resume

# Create your views here.

def upload(request):
    if request.method == "POST":
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            parsed_data = parse_resume(file)
            resume = form.save(commit=False)
            resume.name = parsed_data.get("name", "Unknown")
            resume.email = parsed_data.get("email", "Unknown")
            resume.phone = parsed_data.get("phone", "Unknown")
            resume.save()


            return render(request, "index.html", {"success": True, "data": parsed_data})
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
@parser_classes([MultiPartParser, FormParser])
def index(request):
    """
    API endpoint to handle resume upload and extraction.
    """
    file = request.FILES.get("file")  # Expecting the uploaded file with the key 'file'
    if not file:
        return Response({"error": "No file provided."}, status=400)

    try:
        # Parse the resume
        parsed_data = parse_resume(file)

        # Save the parsed data to the database
        Candidate.objects.create(
            name=parsed_data.get("name", "Unknown"),
            email=parsed_data.get("email", "Unknown"),
            phone=parsed_data.get("phone", "Unknown"),
            file=file,
        )

        # Return only the parsed data
        return Response(parsed_data, status=201)

    except Exception as e:
        return Response({"error": str(e)}, status=500)