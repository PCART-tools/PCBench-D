    def astype(self, dtype, copy: bool = True):
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
            # Ensure that self.astype(self.dtype) is self
            return self.copy() if copy else self

        if (
            self.dtype == np.dtype("M8[ns]")
            and isinstance(dtype, np.dtype)
            and dtype.kind == "M"
            and dtype != np.dtype("M8[ns]")
        ):
            # For now DatetimeArray supports this by unwrapping ndarray,
            #  but DatetimeIndex doesn't
            raise TypeError(f"Cannot cast {type(self).__name__} to dtype")

        values = self._data
        if isinstance(values, ExtensionArray):
            with rewrite_exception(type(values).__name__, type(self).__name__):
                new_values = values.astype(dtype, copy=copy)

        elif isinstance(dtype, ExtensionDtype):
            cls = dtype.construct_array_type()
            # Note: for RangeIndex and CategoricalDtype self vs self._values
            #  behaves differently here.
            new_values = cls._from_sequence(self, dtype=dtype, copy=copy)

        else:
            try:
                new_values = values.astype(dtype, copy=copy)
            except (TypeError, ValueError) as err:
                raise TypeError(
                    f"Cannot cast {type(self).__name__} to dtype {dtype}"
                ) from err

        # pass copy=False because any copying will be done in the astype above
        return Index(new_values, name=self.name, dtype=new_values.dtype, copy=False)
