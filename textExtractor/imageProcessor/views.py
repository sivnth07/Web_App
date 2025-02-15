import pytesseract
from PIL import Image
from django.shortcuts import render, redirect
from .models import ExtractedImage
from .forms import ExtractedImageForm

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def upload_and_extract(request):
    if request.method == "POST":
        form = ExtractedImageForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save(commit=False)
            image = Image.open(uploaded_image.image)
            uploaded_image.extracted_text = pytesseract.image_to_string(image)
            uploaded_image.save()
            return redirect('result', pk=uploaded_image.pk)
    else:
        form = ExtractedImageForm()
    return render(request, 'upload.html', {'form': form})

def result_view(request, pk):
    image_entry = ExtractedImage.objects.get(pk=pk)
    return render(request, 'result.html', {'image_entry': image_entry})

