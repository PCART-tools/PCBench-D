class ReverseStrComparable(object):
    """ Wrap object so that it defaults to string comparison

    Used when sorting in reverse direction.  See StrComparable for normal
    documentation.
    """
    __slots__ = ('obj',)

    def __init__(self, obj):
        self.obj = obj

    def __lt__(self, other):
        try:
            return self.obj > other.obj
        except Exception:
            return str(self.obj) > str(other.obj)
