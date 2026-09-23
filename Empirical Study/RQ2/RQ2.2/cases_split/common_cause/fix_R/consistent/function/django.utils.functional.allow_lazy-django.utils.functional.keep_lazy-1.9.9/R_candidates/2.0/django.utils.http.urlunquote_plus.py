@keep_lazy_text
def urlunquote_plus(quoted_url):
    """
    A legacy compatibility wrapper to Python's urllib.parse.unquote_plus()
    function. (was used for unicode handling on Python 2)
    """
    return unquote_plus(quoted_url)
