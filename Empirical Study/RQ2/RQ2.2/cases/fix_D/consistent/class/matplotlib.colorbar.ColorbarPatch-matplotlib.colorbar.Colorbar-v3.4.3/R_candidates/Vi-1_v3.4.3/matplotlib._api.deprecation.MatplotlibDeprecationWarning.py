class MatplotlibDeprecationWarning(UserWarning):
    """
    A class for issuing deprecation warnings for Matplotlib users.

    In light of the fact that Python builtin DeprecationWarnings are ignored
    by default as of Python 2.7 (see link below), this class was put in to
    allow for the signaling of deprecation, but via UserWarnings which are not
    ignored by default.

    https://docs.python.org/dev/whatsnew/2.7.html#the-future-for-python-2-x
    """
