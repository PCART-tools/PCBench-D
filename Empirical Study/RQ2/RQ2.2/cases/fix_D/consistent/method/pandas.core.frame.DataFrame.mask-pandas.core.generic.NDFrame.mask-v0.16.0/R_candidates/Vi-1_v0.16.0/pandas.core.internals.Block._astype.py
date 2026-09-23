    def _astype(self, dtype, copy=False, raise_on_error=True, values=None,
                klass=None, **kwargs):
        """
        Coerce to the new type (if copy=True, return a new copy)
        raise on an except if raise == True
        """

        # may need to convert to categorical
        # this is only called for non-categoricals
        if self.is_categorical_astype(dtype):
            return make_block(Categorical(self.values, **kwargs),
                              ndim=self.ndim,
                              placement=self.mgr_locs)

        # astype processing
        dtype = np.dtype(dtype)
        if self.dtype == dtype:
            if copy:
                return self.copy()
            return self

        if klass is None:
            if dtype == np.object_:
                klass = ObjectBlock
        try:
            # force the copy here
            if values is None:
                # _astype_nansafe works fine with 1-d only
                values = com._astype_nansafe(self.values.ravel(), dtype, copy=True)
                values = values.reshape(self.values.shape)
            newb = make_block(values,
                              ndim=self.ndim, placement=self.mgr_locs,
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
        return newb
