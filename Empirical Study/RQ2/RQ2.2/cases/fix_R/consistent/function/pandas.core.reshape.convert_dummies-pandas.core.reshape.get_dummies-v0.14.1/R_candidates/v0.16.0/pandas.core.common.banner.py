def banner(message):
    """
    Return 80-char width message declaration with = bars on top and bottom.
    """
    bar = '=' * 80
    return '%s\n%s\n%s' % (bar, message, bar)
