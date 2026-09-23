    def __add__(self, other):
        """
        Composes two transforms together such that *self* is followed
        by *other*.
        """
        if isinstance(other, Transform):
            return composite_transform_factory(self, other)
        raise TypeError(
            "Can not add Transform to object of type '%s'" % type(other))
