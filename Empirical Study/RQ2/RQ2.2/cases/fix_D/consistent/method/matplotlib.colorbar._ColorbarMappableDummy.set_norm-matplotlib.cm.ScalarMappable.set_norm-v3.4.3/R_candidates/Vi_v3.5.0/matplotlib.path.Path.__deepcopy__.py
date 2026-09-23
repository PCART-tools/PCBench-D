    def __deepcopy__(self, memo=None):
        """
        Return a deepcopy of the `Path`.  The `Path` will not be
        readonly, even if the source `Path` is.
        """
        try:
            codes = self.codes.copy()
        except AttributeError:
            codes = None
        return self.__class__(
            self.vertices.copy(), codes,
            _interpolation_steps=self._interpolation_steps)
