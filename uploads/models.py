import os
import base64
import uuid
from django.db import models
from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import BooleanField
# from django.db.models import UUIDField
from django.db.models import TextField

class ImageFile(models.Model):
    # id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_name = CharField(max_length=200)
    file_path = CharField(max_length=200)
    image_url = CharField(max_length=200)
    image_base64 = TextField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    is_deleted = BooleanField(default=False)
    # md5hash

    def __str__(self):
        return self.image_url

    @classmethod
    def create(cls, blob):
        image_base64 = base64.b64encode(blob).decode('utf-8')
        return cls(image_base64=image_base64)

    def deleteFile(self):
        self.is_deleted = True
        os.remove(self.file_path)
        self.save()

    def createFile(self, file_path=None):
        self.is_deleted = False
        if file_path:
            self.file_path = file_path

        directory = os.path.dirname(self.file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(self.file_path, 'wb') as fh:
            blob = base64.b64decode(self.image_base64.encode('utf-8'))
            fh.write(blob)
        self.save()
