#!/bin/bash
set +x

# remove old recources
rm credentials.ini
rm db.sqlite3

# remove old makemigrations
rm wiki/migrations/00*.py
rm uploads/migrations/00*.py
rm characters/migrations/00*.py

# setup db and check for changes
echo "Migrating database..."
python3 manage.py makemigrations
python3 manage.py migrate

# create admin user
if [ ! -f "`pwd`/credentials.ini" ]; then
	echo "Creating admin user..."
	echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@monsters.com', 'dev')" | python3 manage.py shell
	echo "[credentials]
username: admin
password: dev" >> credentials.ini
	cat credentials.ini
fi

# build from current content
echo "
import os
import glob
import base64

from uploads.models import ImageFile
from wiki.models import WikiPage

print('Build database from current content')

print('Importing upload images')
for file in glob.glob('static/images/*'):
    print(' ', file)
    if os.path.isfile(file):
        with open(file, 'rb') as fh:
            blob = fh.read()
            imgFile = ImageFile.create(blob)
            imgFile.file_name = os.path.basename(file)
            imgFile.file_path = file
            imgFile.image_url = '/{0}'.format(file)
            imgFile.save()

print('Importing wiki pages')
for root, dirs, files in os.walk('pages'):
    for file in files:
        file_path = os.path.join(root, file)
        print(' ', file_path)
        wikiPg = WikiPage()
        wikiPg.file_path = file_path
        wikiPg.page_url = file_path.replace('pages/','/wiki/').replace('.md', '')
        with open(file_path, 'r') as fh:
            wikiPg.file_content = fh.read()
        wikiPg.save()

" | python3 manage.py shell
