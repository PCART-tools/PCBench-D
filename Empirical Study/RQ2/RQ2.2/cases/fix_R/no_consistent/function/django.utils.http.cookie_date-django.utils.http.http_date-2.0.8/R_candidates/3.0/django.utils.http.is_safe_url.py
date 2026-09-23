def is_safe_url(url, allowed_hosts, require_https=False):
    warnings.warn(
        'django.utils.http.is_safe_url() is deprecated in favor of '
        'url_has_allowed_host_and_scheme().',
        RemovedInDjango40Warning, stacklevel=2,
    )
    return url_has_allowed_host_and_scheme(url, allowed_hosts, require_https)
