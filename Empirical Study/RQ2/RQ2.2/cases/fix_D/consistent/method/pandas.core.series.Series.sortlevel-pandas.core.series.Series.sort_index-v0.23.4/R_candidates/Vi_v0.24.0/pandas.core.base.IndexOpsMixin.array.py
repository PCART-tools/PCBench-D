    @property
    def array(self):
        # type: () -> ExtensionArray
        """
        The ExtensionArray of the data backing this Series or Index.

        .. versionadded:: 0.24.0

        Returns
        -------
        array : ExtensionArray
            An ExtensionArray of the values stored within. For extension
            types, this is the actual array. For NumPy native types, this
            is a thin (no copy) wrapper around :class:`numpy.ndarray`.

            ``.array`` differs ``.values`` which may require converting the
            data to a different form.

        See Also
        --------
        Index.to_numpy : Similar method that always returns a NumPy array.
        Series.to_numpy : Similar method that always returns a NumPy array.

        Notes
        -----
        This table lays out the different array types for each extension
        dtype within pandas.

        ================== =============================
        dtype              array type
        ================== =============================
        category           Categorical
        period             PeriodArray
        interval           IntervalArray
        IntegerNA          IntegerArray
        datetime64[ns, tz] DatetimeArray
        ================== =============================

        For any 3rd-party extension types, the array type will be an
        ExtensionArray.

        For all remaining dtypes ``.array`` will be a
        :class:`arrays.NumpyExtensionArray` wrapping the actual ndarray
        stored within. If you absolutely need a NumPy array (possibly with
        copying / coercing data), then use :meth:`Series.to_numpy` instead.

        Examples
        --------

        For regular NumPy types like int, and float, a PandasArray
        is returned.

        >>> pd.Series([1, 2, 3]).array
        <PandasArray>
        [1, 2, 3]
        Length: 3, dtype: int64

        For extension types, like Categorical, the actual ExtensionArray
        is returned

        >>> ser = pd.Series(pd.Categorical(['a', 'b', 'a']))
        >>> ser.array
        [a, b, a]
        Categories (2, object): [a, b]
        """
        result = self._values

        if is_datetime64_ns_dtype(result.dtype):
            from pandas.arrays import DatetimeArray
            result = DatetimeArray(result)
        elif is_timedelta64_ns_dtype(result.dtype):
            from pandas.arrays import TimedeltaArray
            result = TimedeltaArray(result)

        elif not is_extension_array_dtype(result.dtype):
            from pandas.core.arrays.numpy_ import PandasArray
            result = PandasArray(result)

        return result
