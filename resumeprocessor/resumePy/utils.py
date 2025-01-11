import re
import pdfplumber
from docx import Document
from docx.shared import Pt

def parse_resume(file):
    """
    Parses the resume file (PDF or DOCX) to extract name, email, and phone number.
    """
    file_name = file.name
    if file_name.endswith('.pdf'):
        text, name = extract_text_from_pdf_with_fonts(file)
    elif file_name.endswith('.docx'):
        text, name = extract_text_from_docx_with_fonts(file)
    else:
        raise ValueError("Unsupported file type. Please upload a PDF or DOCX file.")
    
    # Extract other information
    extracted_info = extract_all_info(text, name)
    return extracted_info

def extract_text_from_pdf_with_fonts(file):
    """Extract text and detect largest font for name from a PDF file."""
    max_font_size = 0
    largest_font_text = None
    full_text = []
    
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            # Extract words with their font sizes
            words = page.extract_words(keep_blank_chars=True, x_tolerance=1, y_tolerance=1)
            
            # Collect all text
            page_text = page.extract_text()
            if page_text:
                full_text.append(page_text)
            
            # Find text with largest font size
            for word in words:
                # Get font size from word properties
                if 'size' in word:
                    font_size = word['size']
                    if font_size > max_font_size:
                        # Check if the word looks like a name (no digits, reasonable length)
                        text = word['text'].strip()
                        if (len(text.split()) <= 3 and 
                            not any(char.isdigit() for char in text) and 
                            len(text) > 3 and 
                            len(text) < 50):
                            max_font_size = font_size
                            largest_font_text = text

    return ' '.join(full_text), largest_font_text

def extract_text_from_docx_with_fonts(file):
    """Extract text and detect largest font for name from a DOCX file."""
    doc = Document(file)
    max_font_size = 0
    largest_font_text = None
    full_text = []
    
    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        full_text.append(text)
        
        # Skip empty paragraphs
        if not text:
            continue
            
        # Check each run in the paragraph for font size
        for run in paragraph.runs:
            if run.font.size is not None:
                # Convert to points if stored in twips (1/20 of a point)
                font_size = run.font.size.pt if isinstance(run.font.size, Pt) else run.font.size / 20
                
                if font_size > max_font_size:
                    # Check if the text looks like a name
                    run_text = run.text.strip()
                    if (len(run_text.split()) <= 3 and 
                        not any(char.isdigit() for char in run_text) and 
                        len(run_text) > 3 and 
                        len(run_text) < 50):
                        max_font_size = font_size
                        largest_font_text = run_text

    return ' '.join(full_text), largest_font_text

def extract_all_info(text, detected_name=None):
    """Extract all information in one pass through the text."""
    # Compile regex patterns
    email_pattern = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
    phone_pattern = re.compile(r'''
        (?:
            (?:\+?\d{1,3}[-.\s]?)?    # Country code
            (?:\(?\d{3}\)?[-.\s]?)?    # Area code
            \d{3}[-.\s]?               # First 3 digits
            \d{4,}                     # Remaining digits (4 or more)
        )
    ''', re.VERBOSE)
    
    # Find email and phone in entire text
    email_matches = email_pattern.findall(text)
    email = email_matches[0] if email_matches else None
    
    phone_matches = phone_pattern.findall(text)
    phone = None
    if phone_matches:
        # Clean up the phone number
        phone = re.sub(r'[\s.-]', '', phone_matches[0])
        if phone.startswith('+'):
            phone = '+' + phone[1:].lstrip('0')
    
    # If no name was detected by font size, try the backup method
    if not detected_name:
        lines = text.split('\n')
        for line in lines[:5]:
            line = line.strip()
            if not line or len(line) > 50:
                continue
            
            words = line.split()
            if 2 <= len(words) <= 3:
                alpha_ratio = sum(c.isalpha() or c.isspace() for c in line) / len(line)
                if alpha_ratio > 0.8:
                    detected_name = line
                    break
    
    return {
        "name": detected_name or "Unknown",
        "email": email,
        "phone": phone,
    }