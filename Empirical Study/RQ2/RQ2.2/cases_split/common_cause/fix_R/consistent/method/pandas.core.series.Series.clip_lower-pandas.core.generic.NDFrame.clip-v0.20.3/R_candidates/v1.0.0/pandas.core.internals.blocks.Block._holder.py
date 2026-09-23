    @property
    def _holder(self):
        """The array-like that can hold the underlying values.

        None for 'Block', overridden by subclasses that don't
        use an ndarray.
        """
        return None
