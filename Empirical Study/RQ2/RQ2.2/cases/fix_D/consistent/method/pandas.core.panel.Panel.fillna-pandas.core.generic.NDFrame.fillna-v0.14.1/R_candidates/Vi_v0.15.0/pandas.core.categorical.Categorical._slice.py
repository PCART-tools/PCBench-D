    def _slice(self, slicer):
        """ Return a slice of myself.

        For internal compatibility with numpy arrays.
        """

        # only allow 1 dimensional slicing, but can
        # in a 2-d case be passd (slice(None),....)
        if isinstance(slicer, tuple) and len(slicer) == 2:
            if not _is_null_slice(slicer[0]):
                raise AssertionError("invalid slicing for a 1-ndim categorical")
            slicer = slicer[1]

        _codes = self._codes[slicer]
        return Categorical(values=_codes,categories=self.categories, ordered=self.ordered,
                           name=self.name, fastpath=True)
