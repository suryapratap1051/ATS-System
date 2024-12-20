from django.shortcuts import render
from django.http import JsonResponse
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to get Gemini output
def get_gemini_output(pdf_text, prompt):
    response = model.generate_content([pdf_text, prompt])
    return response.text

# Function to read PDF
def read_pdf(uploaded_file):
    pdf_reader = PdfReader(uploaded_file)
    pdf_text = ""
    for page in pdf_reader.pages:
        pdf_text += page.extract_text()
    return pdf_text

# Main view
def analyze_resume(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get("resume")
        job_description = request.POST.get("job_description", "")
        analysis_option = request.POST.get("analysis_option", "Quick Scan")
        
        if uploaded_file:
            pdf_text = read_pdf(uploaded_file)
            
            if analysis_option == "Quick Scan":
                prompt = f"""Your quick scan prompt with pdf_text and job_description."""
            elif analysis_option == "Resume Score":
                prompt = f"""Your resume scoring prompt with pdf_text and job_description."""
            elif analysis_option == "Detailed Analysis":
                prompt = f"""Your detailed analysis prompt with pdf_text and job_description."""
            else:  # ATS Optimization
                prompt = f"""Your ATS optimization prompt with pdf_text and job_description."""
            
            response = get_gemini_output(pdf_text, prompt)
            return JsonResponse({"analysis": response})
        else:
            return JsonResponse({"error": "Please upload a resume."})
    
    return render(request, "ats/analyze.html")
