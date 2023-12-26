import json

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import StreamingHttpResponse, FileResponse, JsonResponse
from django.urls import resolve
from django.views.decorators.gzip import gzip_page
from django.views.decorators.http import require_http_methods, require_GET, require_POST, require_safe

from bboard.models import Rubric, Bb


# def index(request):
#     resp_content = ('Здесь будет', ' главная', ' страница', ' сайта')
#     resp = StreamingHttpResponse(resp_content, content_type='text/plain; charset=utf-8')
#     return resp

# def index(request):
#     # file_name = r'static/bg.jpg'
#     file_name = r'static/lesson_15.zip'
#     return FileResponse(open(file_name, 'rb'),
#                         as_attachment=True,
#                         filename='file.zip')

# def index(request):
#     data = {'title': 'Мотоцикл', 'content': 'Старый', 'price': 10000.0}
#     return JsonResponse(data, encoder=DjangoJSONEncoder)

# def index(request):
#     context = {'title': 'Тестовая страница'}
#     return render(request, 'test.html', context)

# def index(request):
#     r = get_object_or_404(Rubric, name="Транспорт")
#     return redirect('bboard:by_rubric', rubric_id=r.id)

# @require_http_methods(['GET', 'POST'])
# @require_GET()
# @require_POST()
# @require_safe()  # GET, HEAD
# @gzip_page()
def index(request):
    rubric = get_object_or_404(Rubric, name="Транспорт")
    bbs = get_list_or_404(Bb, rubric=rubric)

    res = resolve('/2/')

    context = {'title': 'Тестовая страница', 'bbs': bbs, 'res': res}

    return render(request, 'test.html', context)
