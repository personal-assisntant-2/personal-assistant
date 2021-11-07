import codecs
import mimetypes
import os
import pickle

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages

from .forms import CategoryForm, UploadFileForm
from .models import UploadedFiles
from .api import create_uploaded_file, normalize


AUDIO = ['ac3', 'aif', 'mp3', 'ogg', 'wav', 'amr']
ARCHIVE = ['zip', 'tar', 'bztar', 'gztar', 'xztar', 'gz']
DOC = ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx', 'xls', 'docx']
IMG = ['jpeg', 'png', 'jpg', 'svg', 'psd']
VIDEO = ['avi', 'mp4', 'mov', 'mkv']
OTHERS = []


# @login_required(login_url='auth:login')
# def sort_by_category_view(request):
#     form_sort = CategoryForm(request.POST)


# @login_required(login_url='auth:login')
def file_manager_view(request):
    user = User.objects.get(pk=1) # user = request.user

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            handle_uploaded_file(request.FILES['file'], user)
            messages.add_message(request, messages.INFO, 'File was uploaded successfully!')
            return redirect(reverse('file_manager:file'))

        else:
            messages.add_message(request, messages.ERROR, form.errors['file'])
            return render(request, 'file_manager/file.html', {'form': form})

    form = UploadFileForm()
    list_files = UploadedFiles.objects.filter(user=user)
    print('________list_files', list_files)
    return render(request, 'file_manager/file.html', {'form': form, 'list_files': list_files})


# @login_required(login_url='auth:login')
def file_download_view(request, file_id):
    file = get_object_or_404(UploadedFiles, pk=file_id)
    response = HttpResponse(file.file)
    file_type = mimetypes.guess_type(file.name)

    if None in file_type:
        file_type = 'application/octet-stream'

    response['Content-Type'] = file_type
    response['Content-Length'] = str(file.size)
    response['Content-Disposition'] = "attachment; filename=" + normalize(file.name)
    return response


def handle_uploaded_file(f, user):
    file = b''
    for chunk in f.chunks():
        file += chunk

    name = f.name
    extension = f.name.split('.')[-1]
    size = f.size

    with transaction.atomic():
        a = create_uploaded_file(name, extension, file, user, size)

