from django.shortcuts import render


def handler400(request, exception):
    try:
        context = {}
        response = render(request, "errors/400.html", context=context)
        response.status_code = 400
        return response
    except exception as e:
        print(e)


def handler403(request, exception):
    try:
        context = {}
        response = render(request, "errors/403.html", context=context)
        response.status_code = 403
        return response
    except exception as e:
        print(e)


def handler404(request, exception):
    try:
        context = {}
        response = render(request, "errors/404.html", context=context)
        response.status_code = 404
        return response
    except exception as e:
        print(e)


def handler500(request):
    context = {}
    response = render(request, "errors/500.html", context=context)
    response.status_code = 500
    return response
