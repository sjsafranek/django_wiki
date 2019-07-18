import os
import uuid
from django.db import models
from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import BooleanField
from django.db.models import TextField
from django.db.models import UUIDField

class WikiPage(models.Model):
    # id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    page_url = models.CharField(max_length=200, editable=False)
    file_path = models.CharField(max_length=200)
    file_content = models.TextField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    is_deleted = BooleanField(default=False)
    # md5hash

    class Meta:
        unique_together = (('page_url', 'created_at'))

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

        with open(self.file_path, 'w') as fh:
            fh.write(self.file_content)
        self.save()


def fetchWikiPage(file_path, create_if_not_exists=False):
    pages = WikiPage.objects.filter(file_path=file_path, is_deleted=False)
    if 0 != len(pages):
        if 1 != len(pages):
            raise ValueError("DatabaseError: Multiple pages found")
        return pages[0]
    if not create_if_not_exists:
        return None
    return WikiPage()
