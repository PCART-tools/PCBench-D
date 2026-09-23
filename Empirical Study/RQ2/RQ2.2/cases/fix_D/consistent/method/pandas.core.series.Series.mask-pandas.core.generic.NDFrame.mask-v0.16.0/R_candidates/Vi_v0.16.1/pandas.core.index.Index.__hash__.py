    def __hash__(self):
        raise TypeError("unhashable type: %r" % type(self).__name__)
