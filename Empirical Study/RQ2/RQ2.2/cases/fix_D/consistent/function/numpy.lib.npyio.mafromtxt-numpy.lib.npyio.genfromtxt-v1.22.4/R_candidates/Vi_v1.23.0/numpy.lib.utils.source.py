@set_module('numpy')
def source(object, output=sys.stdout):
    """
    Print or write to a file the source code for a NumPy object.

    The source code is only returned for objects written in Python. Many
    functions and classes are defined in C and will therefore not return
    useful information.

    Parameters
    ----------
    object : numpy object
        Input object. This can be any object (function, class, module,
        ...).
    output : file object, optional
        If `output` not supplied then source code is printed to screen
        (sys.stdout).  File object must be created with either write 'w' or
        append 'a' modes.

    See Also
    --------
    lookfor, info

    Examples
    --------
    >>> np.source(np.interp)                        #doctest: +SKIP
    In file: /usr/lib/python2.6/dist-packages/numpy/lib/function_base.py
    def interp(x, xp, fp, left=None, right=None):
        \"\"\".... (full docstring printed)\"\"\"
        if isinstance(x, (float, int, number)):
            return compiled_interp([x], xp, fp, left, right).item()
        else:
            return compiled_interp(x, xp, fp, left, right)

    The source code is only returned for objects written in Python.

    >>> np.source(np.array)                         #doctest: +SKIP
    Not available for this object.

    """
    # Local import to speed up numpy's import time.
    import inspect
    try:
        print("In file: %s\n" % inspect.getsourcefile(object), file=output)
        print(inspect.getsource(object), file=output)
    except Exception:
        print("Not available for this object.", file=output)
