    def astype(self, dtype, copy=True):
        """
        Coerce this type to another dtype

        Parameters
        ----------
        dtype : numpy dtype or pandas type
        copy : bool, default True
            By default, astype always returns a newly allocated object.
            If copy is set to False and dtype is categorical, the original
            object is returned.

            .. versionadded:: 0.19.0

        """
        if is_categorical_dtype(dtype):
            # GH 10696/18593
            dtype = self.dtype.update_dtype(dtype)
            self = self.copy() if copy else self
            if dtype == self.dtype:
                return self
            return self._set_dtype(dtype)
        return np.array(self, dtype=dtype, copy=copy)
