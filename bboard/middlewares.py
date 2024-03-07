from django.db.models import Count

from bboard.models import Rubric


def my_middleware(_next):
    # Здесь можно выполнить какую-либо инициализацию
    def core_middleware(request):
        # Обработка клиентского запроса
        response = _next(request)
        print('Р А Б О Т А Е Т !')
        # Обработка ответа
        return response
    return core_middleware


class MyMiddleware:
    def __init__(self, get_response):
        self._next = get_response
        # Здесь можно выполнить какую-либо инициализацию

    def __call__(self, request):
        # Обработка клиентского запроса
        response = self._next(request)
        # Обработка ответа
        return response


class RubricMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        return self._get_response(request)

    def process_template_response(self, request, response):
        # response.context_data['rubrics'] = Rubric.objects.all()
        response.context_data['rubrics'] = Rubric.objects.annotate(
            cnt=Count('bb')).filter(cnt__gt=0)
        return response


def rubrics(request):
    return {
        'rubrics': Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
    }
