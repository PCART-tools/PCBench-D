    class MockSplitter:
        def __init__(self, a, b=0, c=None):
            self.a = a
            self.b = b
            self.c = c

        def __repr__(self):
            return _build_repr(self)
