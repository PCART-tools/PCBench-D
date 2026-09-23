    def __array_wrap__(self, result, context=None):
        # we don't want the superclass implementation
        return result
