@keep_lazy_text
def urlquote_plus(url, safe=''):
    """
    A legacy compatibility wrapper to Python's urllib.parse.quote_plus()
    function. (was used for unicode handling on Python 2)
    """
    warnings.warn(
        'django.utils.http.urlquote_plus() is deprecated in favor of '
        'urllib.parse.quote_plus(),',
        RemovedInDjango40Warning, stacklevel=2,
    )
    return quote_plus(url, safe)
