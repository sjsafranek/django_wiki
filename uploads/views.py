import os.path
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from . import models

# delete_imagefile

@login_required(login_url='/login')
@permission_required('uploads.add_imagefile', raise_exception=True)
@permission_required('uploads.change_imagefile', raise_exception=True)
def uploadFileHandler(request):
    uploaded_files = []
    if "POST" == request.method:
        # save files
        section = request.POST['section']
        for key, file in request.FILES.items():
            file_path = os.path.join('static', section, file.name)

            directory = os.path.dirname(file_path)
            if not os.path.exists(directory):
                os.makedirs(directory)

            with open(file_path, 'wb') as dest:
                if file.multiple_chunks:
                    for c in file.chunks():
                        dest.write(c)
                else:
                    dest.write(file.read())
            uploaded_files.append(file_path)

            with open(file_path, 'rb') as fh:
                blob = fh.read()
                imgFile = models.ImageFile.create(blob)
                imgFile.file_name = file.name
                imgFile.file_path = file_path
                imgFile.image_url = '/{0}'.format(file_path)
                imgFile.save()

    # return response
    return render(request,'upload_files.html', {
        'uploaded_files': uploaded_files
    })
