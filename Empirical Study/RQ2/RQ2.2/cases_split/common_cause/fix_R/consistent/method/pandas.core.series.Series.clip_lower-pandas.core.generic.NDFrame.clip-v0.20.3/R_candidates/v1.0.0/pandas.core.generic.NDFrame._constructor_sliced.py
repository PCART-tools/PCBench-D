    @property
    def _constructor_sliced(self):
        """Used when a manipulation result has one lower dimension(s) as the
        original, such as DataFrame single columns slicing.
        """
        raise AbstractMethodError(self)
