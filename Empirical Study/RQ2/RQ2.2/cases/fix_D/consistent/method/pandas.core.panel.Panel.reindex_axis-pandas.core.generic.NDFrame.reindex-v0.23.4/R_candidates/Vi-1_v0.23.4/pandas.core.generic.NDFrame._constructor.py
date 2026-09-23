    @property
    def _constructor(self):
        """Used when a manipulation result has the same dimensions as the
        original.
        """
        raise com.AbstractMethodError(self)
