from wiki.models import WikiPage
from uploads.models import ImageFile

def restorePages():
    for page in WikiPage.objects.filter(is_deleted=False).all():
        print("CREATE", page.file_path)
        page.createFile()

def restoreImages():
    for image in ImageFile.objects.filter(is_deleted=False).all():
        print("CREATE", image.file_path)
        image.createFile()

def restoreAll():
    restorePages()
    restoreImages()
