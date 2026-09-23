def _generate_cache_key(request, method, headerlist, key_prefix):
    """Return a cache key from the headers given in the header list."""
    ctx = hashlib.md5()
    for header in headerlist:
        value = request.META.get(header)
        if value is not None:
            ctx.update(value.encode())
    url = hashlib.md5(request.build_absolute_uri().encode('ascii'))
    cache_key = 'views.decorators.cache.cache_page.%s.%s.%s.%s' % (
        key_prefix, method, url.hexdigest(), ctx.hexdigest())
    return _i18n_cache_key_suffix(request, cache_key)
