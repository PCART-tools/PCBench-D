def get_system_encoding():
    """
    The encoding of the default system locale. Fallback to 'ascii' if the
    #encoding is unsupported by Python or could not be determined. See tickets
    #10335 and #5846.
    """
    try:
        encoding = locale.getdefaultlocale()[1] or 'ascii'
        codecs.lookup(encoding)
    except Exception:
        encoding = 'ascii'
    return encoding
