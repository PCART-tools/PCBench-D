def patch_response_headers(response, cache_timeout=None):
    """
    Add HTTP caching headers to the given HttpResponse: Expires and
    Cache-Control.

    Each header is only added if it isn't already set.

    cache_timeout is in seconds. The CACHE_MIDDLEWARE_SECONDS setting is used
    by default.
    """
    if cache_timeout is None:
        cache_timeout = settings.CACHE_MIDDLEWARE_SECONDS
    if cache_timeout < 0:
        cache_timeout = 0  # Can't have max-age negative
    if settings.USE_ETAGS and not response.has_header('ETag'):
        warnings.warn(
            "The USE_ETAGS setting is deprecated in favor of "
            "ConditionalGetMiddleware which sets the ETag regardless of the "
            "setting. patch_response_headers() won't do ETag processing in "
            "Django 2.1.",
            RemovedInDjango21Warning
        )
        if hasattr(response, 'render') and callable(response.render):
            response.add_post_render_callback(set_response_etag)
        else:
            response = set_response_etag(response)
    if not response.has_header('Expires'):
        response['Expires'] = http_date(time.time() + cache_timeout)
    patch_cache_control(response, max_age=cache_timeout)
