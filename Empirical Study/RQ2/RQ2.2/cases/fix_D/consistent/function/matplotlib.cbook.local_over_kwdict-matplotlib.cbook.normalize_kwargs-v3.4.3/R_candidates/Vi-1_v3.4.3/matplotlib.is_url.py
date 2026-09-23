def is_url(filename):
    """Return whether *filename* is an http, https, ftp, or file URL path."""
    return URL_REGEX.match(filename) is not None
