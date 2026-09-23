    def __call__(self, x, pos=None):
        """
        Return the format for tick value `x` at position pos.
        ``pos=None`` indicates an unspecified location.
        """
        raise NotImplementedError('Derived must override')
