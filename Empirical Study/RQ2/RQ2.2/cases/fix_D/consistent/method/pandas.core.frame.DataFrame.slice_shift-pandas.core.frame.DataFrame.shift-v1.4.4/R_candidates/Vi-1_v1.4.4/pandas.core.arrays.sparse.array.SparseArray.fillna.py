    def fillna(
        self: SparseArrayT,
        value=None,
        method: FillnaOptions | None = None,
        limit: int | None = None,
    ) -> SparseArrayT:
        """
        Fill missing values with `value`.

        Parameters
        ----------
        value : scalar, optional
        method : str, optional

            .. warning::

               Using 'method' will result in high memory use,
               as all `fill_value` methods will be converted to
               an in-memory ndarray

        limit : int, optional

        Returns
        -------
        SparseArray

        Notes
        -----
        When `value` is specified, the result's ``fill_value`` depends on
        ``self.fill_value``. The goal is to maintain low-memory use.

        If ``self.fill_value`` is NA, the result dtype will be
        ``SparseDtype(self.dtype, fill_value=value)``. This will preserve
        amount of memory used before and after filling.

        When ``self.fill_value`` is not NA, the result dtype will be
        ``self.dtype``. Again, this preserves the amount of memory used.
        """
        if (method is None and value is None) or (
            method is not None and value is not None
        ):
            raise ValueError("Must specify one of 'method' or 'value'.")

        elif method is not None:
            msg = "fillna with 'method' requires high memory usage."
            warnings.warn(msg, PerformanceWarning)
            # Need type annotation for "new_values"  [var-annotated]
            new_values = np.asarray(self)  # type: ignore[var-annotated]
            # interpolate_2d modifies new_values inplace
            interpolate_2d(new_values, method=method, limit=limit)
            return type(self)(new_values, fill_value=self.fill_value)

        else:
            new_values = np.where(isna(self.sp_values), value, self.sp_values)

            if self._null_fill_value:
                # This is essentially just updating the dtype.
                new_dtype = SparseDtype(self.dtype.subtype, fill_value=value)
            else:
                new_dtype = self.dtype

        return self._simple_new(new_values, self._sparse_index, new_dtype)
