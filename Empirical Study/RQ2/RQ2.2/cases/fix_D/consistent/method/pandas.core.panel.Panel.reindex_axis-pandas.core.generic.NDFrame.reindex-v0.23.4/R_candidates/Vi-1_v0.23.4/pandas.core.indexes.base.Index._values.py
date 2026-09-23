    @property
    def _values(self):
        # type: () -> Union[ExtensionArray, Index]
        # TODO(EA): remove index types as they become extension arrays
        """The best array representation.

        This is an ndarray, ExtensionArray, or Index subclass. This differs
        from ``_ndarray_values``, which always returns an ndarray.

        Both ``_values`` and ``_ndarray_values`` are consistent between
        ``Series`` and ``Index``.

        It may differ from the public '.values' method.

        index             | values          | _values     | _ndarray_values |
        ----------------- | -------------- -| ----------- | --------------- |
        CategoricalIndex  | Categorical     | Categorical | codes           |
        DatetimeIndex[tz] | ndarray[M8ns]   | DTI[tz]     | ndarray[M8ns]   |

        For the following, the ``._values`` is currently ``ndarray[object]``,
        but will soon be an ``ExtensionArray``

        index             | values          | _values      | _ndarray_values |
        ----------------- | --------------- | ------------ | --------------- |
        PeriodIndex       | ndarray[object] | ndarray[obj] | ndarray[int]    |
        IntervalIndex     | ndarray[object] | ndarray[obj] | ndarray[object] |

        See Also
        --------
        values
        _ndarray_values
        """
        return self.values
