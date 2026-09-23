    def _astype(self, dtype, copy=False, raise_on_error=True, values=None,
                klass=None):
        """
        Coerce to the new type (if copy=True, return a new copy)
        raise on an except if raise == True
        """
        dtype = np.dtype(dtype)
        if self.dtype == dtype:
            if copy:
                return self.copy()
            return self

        try:
            # force the copy here
            if values is None:
                values = com._astype_nansafe(self.values, dtype, copy=True)
            newb = make_block(values, self.items, self.ref_items,
                              ndim=self.ndim, placement=self._ref_locs,
                              fastpath=True, dtype=dtype, klass=klass)
        except:
            if raise_on_error is True:
                raise
            newb = self.copy() if copy else self

        if newb.is_numeric and self.is_numeric:
            if newb.shape != self.shape:
                raise TypeError("cannot set astype for copy = [%s] for dtype "
                                "(%s [%s]) with smaller itemsize that current "
                                "(%s [%s])" % (copy, self.dtype.name,
                                               self.itemsize, newb.dtype.name,
                                               newb.itemsize))
        return [newb]
