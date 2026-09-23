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
            if copy is True:
                return self.copy()
            return self
        return np.array(self, dtype=dtype, copy=copy)
