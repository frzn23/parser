Resume Parser - Readme

This is a Python-based resume parsing application that can extract key information from resume documents (PDF and DOCX formats). 

Features

* Extracts name, email, and phone number from resumes.
* Handles resumes in both PDF and DOCX formats.
* Uses regular expressions and font size heuristics to identify relevant information.

Dependencies

This application relies on the following Python libraries:

* pdfplumber: For parsing PDF files.
* docx: For parsing DOCX files.
* re: For regular expressions.

Usage

1. Installation

bash
pip install -r requirements.txt


2. Running the application (Web API)

This application provides a web API endpoint to handle resume upload and parsing. 

* Upload a resume file using the file field in a multipart form data request.
* The API will return a JSON response containing the extracted information (name, email, phone number).

3. Running the application (Django view)

* Implement a Django view to handle form submission and file upload.
* Use the parse_resume function fromutils.py to extract information from the uploaded file.
* Render a template with the extracted information.

4. utils.py

This module contains the core functionality for resume parsing.

parse_resume(file): This function takes a resume file as input and returns a dictionary containing the extracted information (name, email, phone number).

5. views.py

This module defines the Django views for handling resume upload and parsing.

* upload(request): This view handles form submission and file upload.
* It uses the 'parse_resume' function to extract information from the uploaded file.
* It renders a template with the extracted information.

6. requirements.txt

This file specifies the required Python libraries and their versions.

