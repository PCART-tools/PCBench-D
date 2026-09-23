@keep_lazy_text
def urlquote_plus(url, safe=''):
    """
    A legacy compatibility wrapper to Python's urllib.parse.quote_plus()
    function. (was used for unicode handling on Python 2)
    """
    return quote_plus(url, safe)
