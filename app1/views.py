import os

import pycodestyle
from django.shortcuts import render
from .forms import FileUploadForm
from .models import CheckedFile


def home(request):
    form = FileUploadForm()
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            file_path = os.path.join('/tmp', uploaded_file.name)
            with open(file_path, 'wb') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)
            style = pycodestyle.StyleGuide()
            result = style.check_files([file_path])
            os.remove(file_path)
            if result.total_errors == 0:
                pep8_compliant = True
            else:
                pep8_compliant = False
            CheckedFile.objects.create(
                name=uploaded_file.name,
                content=uploaded_file.read().decode('utf-8'),
                pep8_compliant=pep8_compliant,
            )
    files = CheckedFile.objects.all()
    return render(request, 'home.html', {'form': form, 'files': files})