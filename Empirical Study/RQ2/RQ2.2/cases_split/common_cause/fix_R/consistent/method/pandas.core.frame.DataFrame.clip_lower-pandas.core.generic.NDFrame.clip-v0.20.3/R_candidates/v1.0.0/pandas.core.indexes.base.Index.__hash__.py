    def __hash__(self):
        raise TypeError(f"unhashable type: {repr(type(self).__name__)}")
