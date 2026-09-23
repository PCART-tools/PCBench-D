@keep_lazy_text
def urlquote(url, safe='/'):
    """
    A legacy compatibility wrapper to Python's urllib.parse.quote() function.
    (was used for unicode handling on Python 2)
    """
    return quote(url, safe)
