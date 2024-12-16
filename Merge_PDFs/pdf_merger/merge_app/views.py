from django.shortcuts import render
from django.http import FileResponse
import os
from PyPDF2 import PdfMerger

def index(request):
    return render(request, 'index.html')

def merge_pdfs(request):
    if request.method == 'POST':
        pdf_merger = PdfMerger()
        files = request.FILES.getlist('pdf_files')
        
        for pdf in files:
            pdf_merger.append(pdf)

        # Save the merged PDF
        merged_file_path = 'merged_output.pdf'
        with open(merged_file_path, 'wb') as merged_file:
            pdf_merger.write(merged_file)

        pdf_merger.close()
        
        # Return the merged file as a response
        response = FileResponse(open(merged_file_path, 'rb'), as_attachment=True, filename='merged_file.pdf')
        return response