def _precondition_failed(request):
    logger.warning(
        'Precondition Failed: %s', request.path,
        extra={
            'status_code': 412,
            'request': request,
        },
    )
    return HttpResponse(status=412)
