    @property
    def _values(self) -> Union[ExtensionArray, ABCIndexClass, np.ndarray]:
        # TODO(EA): remove index types as they become extension arrays
        """
        The best array representation.

        This is an ndarray, ExtensionArray, or Index subclass. This differs
        from ``_ndarray_values``, which always returns an ndarray.

        Both ``_values`` and ``_ndarray_values`` are consistent between
        ``Series`` and ``Index``.

        It may differ from the public '.values' method.

        index             | values          | _values       | _ndarray_values |
        ----------------- | --------------- | ------------- | --------------- |
        Index             | ndarray         | ndarray       | ndarray         |
        CategoricalIndex  | Categorical     | Categorical   | ndarray[int]    |
        DatetimeIndex     | ndarray[M8ns]   | ndarray[M8ns] | ndarray[M8ns]   |
        DatetimeIndex[tz] | ndarray[M8ns]   | DTI[tz]       | ndarray[M8ns]   |
        PeriodIndex       | ndarray[object] | PeriodArray   | ndarray[int]    |
        IntervalIndex     | IntervalArray   | IntervalArray | ndarray[object] |

        See Also
        --------
        values
        _ndarray_values
        """
        return self._data
