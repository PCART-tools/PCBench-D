    def astype(self, dtype, copy=True, raise_on_error=True, **kwargs):
        """
        Cast object to input numpy.dtype
        Return a copy when copy = True (be really careful with this!)

        Parameters
        ----------
        dtype : numpy.dtype or Python type
        raise_on_error : raise on invalid input
        kwargs : keyword arguments to pass on to the constructor

        Returns
        -------
        casted : type of caller
        """

        mgr = self._data.astype(
            dtype=dtype, copy=copy, raise_on_error=raise_on_error, **kwargs)
        return self._constructor(mgr).__finalize__(self)
