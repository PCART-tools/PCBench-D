def _generate_cache_header_key(key_prefix, request):
    """Return a cache key for the header cache."""
    url = hashlib.md5(request.build_absolute_uri().encode('ascii'))
    cache_key = 'views.decorators.cache.cache_header.%s.%s' % (
        key_prefix, url.hexdigest())
    return _i18n_cache_key_suffix(request, cache_key)
