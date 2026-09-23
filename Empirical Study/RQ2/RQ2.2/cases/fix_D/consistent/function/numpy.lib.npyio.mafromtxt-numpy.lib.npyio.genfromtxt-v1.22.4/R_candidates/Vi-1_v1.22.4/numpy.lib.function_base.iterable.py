@set_module('numpy')
def iterable(y):
    """
    Check whether or not an object can be iterated over.

    Parameters
    ----------
    y : object
      Input object.

    Returns
    -------
    b : bool
      Return ``True`` if the object has an iterator method or is a
      sequence and ``False`` otherwise.


    Examples
    --------
    >>> np.iterable([1, 2, 3])
    True
    >>> np.iterable(2)
    False

    Notes
    -----
    In most cases, the results of ``np.iterable(obj)`` are consistent with
    ``isinstance(obj, collections.abc.Iterable)``. One notable exception is
    the treatment of 0-dimensional arrays::

        >>> from collections.abc import Iterable
        >>> a = np.array(1.0)  # 0-dimensional numpy array
        >>> isinstance(a, Iterable)
        True
        >>> np.iterable(a)
        False

    """
    try:
        iter(y)
    except TypeError:
        return False
    return True
