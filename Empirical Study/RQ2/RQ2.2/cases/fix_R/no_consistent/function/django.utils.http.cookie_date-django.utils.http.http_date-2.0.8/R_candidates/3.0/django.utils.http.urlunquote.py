@keep_lazy_text
def urlunquote(quoted_url):
    """
    A legacy compatibility wrapper to Python's urllib.parse.unquote() function.
    (was used for unicode handling on Python 2)
    """
    warnings.warn(
        'django.utils.http.urlunquote() is deprecated in favor of '
        'urllib.parse.unquote().',
        RemovedInDjango40Warning, stacklevel=2,
    )
    return unquote(quoted_url)
