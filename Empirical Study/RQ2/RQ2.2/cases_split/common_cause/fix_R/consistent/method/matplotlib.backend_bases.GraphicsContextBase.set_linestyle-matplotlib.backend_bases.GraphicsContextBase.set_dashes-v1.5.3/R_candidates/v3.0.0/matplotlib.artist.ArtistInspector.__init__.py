    def __init__(self, o):
        r"""
        Initialize the artist inspector with an `Artist` or an iterable of
        `Artist`\s.  If an iterable is used, we assume it is a homogeneous
        sequence (all `Artists` are of the same type) and it is your
        responsibility to make sure this is so.
        """
        if not isinstance(o, Artist):
            if cbook.iterable(o):
                o = list(o)
                if len(o):
                    o = o[0]

        self.oorig = o
        if not inspect.isclass(o):
            o = type(o)
        self.o = o

        self.aliasd = self.get_aliases()
