    @property
    def shape(self) -> Shape:
        """
        Return a tuple of the shape of the underlying data.
        """
        # not using "(len(self), )" to return "correct" shape if the values
        # consists of a >1 D array (see GH-27775)
        # overridden in MultiIndex.shape to avoid materializing the values
        return self._values.shape
