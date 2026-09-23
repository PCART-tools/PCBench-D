def npath(path):
    """
    Always return a native path, that is unicode on Python 3 and bytestring on
    Python 2. Noop for Python 3.
    """
    return path
