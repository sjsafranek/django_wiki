import json
import os
import os.path
from django.template import loader
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import JsonResponse

# Import the login_required decorator which can be applied to views
# to enforce that the user should be logged in to access the view
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

import markdown

from .models import fetchWikiPage


def page2file_path(request_path):
    file_path = request_path.replace('/wiki/', 'pages/').replace('/edit', '').replace('/delete', '')
    if os.path.exists(file_path) and os.path.isdir(file_path):
        file_path = os.path.join(file_path, 'index')
    file_path += '.md'
    return file_path

def delete_page(request_path):
    file_path = page2file_path(request_path)
    # mark record as deleted
    wikiPg = fetchWikiPage(file_path)
    if wikiPg:
        wikiPg.deleteFile()
        return {"status":"ok", "data":{"message":"page marked as deleted"}}
    return {"status":"error", "error":"page not found"}
    #.end

def save_page_content(request_path, page_content):
    file_path = page2file_path(request_path)

    # update or create record
    wikiPg = fetchWikiPage(file_path, create_if_not_exists=True)
    wikiPg.file_path = file_path
    wikiPg.page_url = request_path
    wikiPg.file_content = page_content
    wikiPg.is_deleted = False
    wikiPg.save()
    #.end

    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(file_path, 'w') as fh:
        fh.write(page_content)

def get_page_content_html(request_path):
    file_path = page2file_path(request_path)
    if not os.path.exists(file_path):
        return ''
    with open(file_path, 'r') as fh:
        md = fh.read()
        # extensions = ['extra', 'smarty']
        # html = markdown.markdown(md, extensions=extensions, output_format='html5')
        html = markdown.markdown(md, output_format='html5')
        return html

def get_page_content_md(request_path):
    file_path = page2file_path(request_path)
    if not os.path.exists(file_path):
        return ''
    with open(file_path, 'r') as fh:
        return fh.read()


def get_content_directory_tree():
    data = {}
    for root, dirs, files in os.walk('pages'):
        link = root.replace('pages', 'wiki')
        _files = []
        for file in files:
            _files.append({
                'href': '/{0}/{1}'.format(link, file.replace('.md', '')),
                'name': file.replace('.md', '')
            })
        parts = link.split('/')
        _path = data
        for i in range(len(parts)):
            if parts[i] not in _path:
                _path[parts[i]] = {
                    'dirs': {},
                    'files': _files,
                    'href': '/{0}'.format(link),
                    'name': parts[i]
                }
            _path = _path[parts[i]]['dirs']
    return data




def methodNotAllowedResponse():
    return JsonResponse({"status":"error", "error":"method not allowed"}, status=405)


def viewPageHandler(request):
    if "GET" == request.method:
        page_content = get_page_content_html(request.path)
        tmpl = loader.get_template('view_page.html')
        context = {
            'page_content': page_content,
            'navigation': get_content_directory_tree()
        }
        html = tmpl.render(context)
        return HttpResponse(html)
    else:
        return methodNotAllowedResponse()


@csrf_exempt
@login_required(login_url='/login')
@permission_required('wiki.add_wikipage', raise_exception=True)
@permission_required('wiki.change_wikipage', raise_exception=True)
def editPageHandler(request):
    if "GET" == request.method:
        md = get_page_content_md(request.path)
        tmpl = loader.get_template('edit_page.html')
        context = {'md': md}
        html = tmpl.render(context)
        return HttpResponse(html)
    elif "POST" == request.method:
        # get data
        data = json.loads(request.body.decode('utf-8'))
        # save page
        save_page_content(request.path, data['content'])
        # send api response
        return JsonResponse({"status":"ok"})
    else:
        return methodNotAllowedResponse()


@csrf_exempt
@login_required(login_url='/login')
@permission_required('WikiPage.delete_wikipage', raise_exception=True)
def deletePageHandler(request):
    if "DELETE" == request.method:
        # TODO
        results = delete_page(request.path)
        return JsonResponse(results)
    else:
        return methodNotAllowedResponse()







#
