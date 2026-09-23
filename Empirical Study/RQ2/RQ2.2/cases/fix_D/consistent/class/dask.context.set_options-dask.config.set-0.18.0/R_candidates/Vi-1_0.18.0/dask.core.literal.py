class literal(object):
    """A small serializable object to wrap literal values without copying"""
    __slots__ = ('data',)

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return 'literal<type=%s>' % type(self.data).__name__

    def __reduce__(self):
        return (literal, (self.data,))

    def __call__(self):
        return self.data
