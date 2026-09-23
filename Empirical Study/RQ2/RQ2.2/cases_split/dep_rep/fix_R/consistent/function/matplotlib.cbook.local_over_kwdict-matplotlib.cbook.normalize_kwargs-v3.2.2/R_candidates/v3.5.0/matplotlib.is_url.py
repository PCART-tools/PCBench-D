@_api.deprecated("3.5")
def is_url(filename):
    """Return whether *filename* is an http, https, ftp, or file URL path."""
    return __getattr__("URL_REGEX").match(filename) is not None
