from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.contrib import messages
from .models import SharedFile
from .forms import FileUploadForm


@login_required
def file_list(request):
    files = SharedFile.objects.select_related('user').all()
    query = request.GET.get('q', '')
    if query:
        files = files.filter(title__icontains=query)
    form = FileUploadForm()
    return render(request, 'files/upload.html', {'files': files, 'form': form, 'query': query})


@login_required
def file_upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            fname = request.FILES['file'].name.lower()
            if fname.endswith('.pdf'):
                f.file_type = 'pdf'
            elif fname.endswith(('.doc', '.docx', '.txt')):
                f.file_type = 'doc'
            elif fname.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                f.file_type = 'img'
            else:
                f.file_type = 'other'
            f.save()
            messages.success(request, 'File uploaded successfully!')
    return redirect('file_list')


@login_required
def file_download(request, file_id):
    shared_file = get_object_or_404(SharedFile, id=file_id)
    shared_file.download_count += 1
    shared_file.save()
    return FileResponse(shared_file.file.open(), as_attachment=True, filename=shared_file.filename())


@login_required
def file_delete(request, file_id):
    shared_file = get_object_or_404(SharedFile, id=file_id, user=request.user)
    shared_file.file.delete()
    shared_file.delete()
    messages.success(request, 'File deleted.')
    return redirect('file_list')