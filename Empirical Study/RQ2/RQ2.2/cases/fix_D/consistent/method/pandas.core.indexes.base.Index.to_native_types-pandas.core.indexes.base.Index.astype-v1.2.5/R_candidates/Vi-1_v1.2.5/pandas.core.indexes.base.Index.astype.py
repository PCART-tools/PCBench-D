    def astype(self, dtype, copy=True):
        """
        Create an Index with values cast to dtypes.

        The class of a new Index is determined by dtype. When conversion is
        impossible, a TypeError exception is raised.

        Parameters
        ----------
        dtype : numpy dtype or pandas type
            Note that any signed integer `dtype` is treated as ``'int64'``,
            and any unsigned integer `dtype` is treated as ``'uint64'``,
            regardless of the size.
        copy : bool, default True
            By default, astype always returns a newly allocated object.
            If copy is set to False and internal requirements on dtype are
            satisfied, the original data is used to create a new Index
            or the original Index is returned.

        Returns
        -------
        Index
            Index with values cast to specified dtype.
        """
        if dtype is not None:
            dtype = pandas_dtype(dtype)

        if is_dtype_equal(self.dtype, dtype):
            return self.copy() if copy else self

        elif is_categorical_dtype(dtype):
            from pandas.core.indexes.category import CategoricalIndex

            return CategoricalIndex(
                self._values, name=self.name, dtype=dtype, copy=copy
            )

        elif is_extension_array_dtype(dtype):
            return Index(np.asarray(self), name=self.name, dtype=dtype, copy=copy)

        try:
            casted = self._values.astype(dtype, copy=copy)
        except (TypeError, ValueError) as err:
            raise TypeError(
                f"Cannot cast {type(self).__name__} to dtype {dtype}"
            ) from err
        return Index(casted, name=self.name, dtype=dtype)
