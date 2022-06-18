from django.shortcuts import render


def handler400(request, exception):
    context = {}
    response = render(request, "errors/400.html", context=context)
    response.status_code = 400
    return response


def handler403(request, exception):
    context = {}
    response = render(request, "errors/403.html", context=context)
    response.status_code = 403
    return response


def handler404(request, exception):
    context = {}
    response = render(request, "errors/404.html", context=context)
    response.status_code = 404
    return response


def handler500(request):
    context = {}
    response = render(request, "errors/500.html", context=context)
    response.status_code = 500
    return response
