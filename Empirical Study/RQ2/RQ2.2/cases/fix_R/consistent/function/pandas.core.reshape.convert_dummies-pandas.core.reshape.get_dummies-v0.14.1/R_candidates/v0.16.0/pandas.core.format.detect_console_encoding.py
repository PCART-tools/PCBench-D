def detect_console_encoding():
    """
    Try to find the most capable encoding supported by the console.
    slighly modified from the way IPython handles the same issue.
    """
    import locale
    global _initial_defencoding

    encoding = None
    try:
        encoding = sys.stdout.encoding or sys.stdin.encoding
    except AttributeError:
        pass

    # try again for something better
    if not encoding or 'ascii' in encoding.lower():
        try:
            encoding = locale.getpreferredencoding()
        except Exception:
            pass

    # when all else fails. this will usually be "ascii"
    if not encoding or 'ascii' in encoding.lower():
        encoding = sys.getdefaultencoding()

    # GH3360, save the reported defencoding at import time
    # MPL backends may change it. Make available for debugging.
    if not _initial_defencoding:
        _initial_defencoding = sys.getdefaultencoding()

    return encoding
