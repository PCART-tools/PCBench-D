class StrComparable(object):
    """ Wrap object so that it defaults to string comparison

    When comparing two objects of different types Python fails

    >>> 'a' < 1  # doctest: +SKIP
    Traceback (most recent call last):
        ...
    TypeError: '<' not supported between instances of 'str' and 'int'

    This class wraps the object so that, when this would occur it instead
    compares the string representation

    >>> StrComparable('a') < StrComparable(1)
    False
    """
    __slots__ = ('obj',)

    def __init__(self, obj):
        self.obj = obj

    def __lt__(self, other):
        try:
            return self.obj < other.obj
        except Exception:
            return str(self.obj) < str(other.obj)
