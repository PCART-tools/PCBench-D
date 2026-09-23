    @property
    def _values(self):
        """
        Return the internal repr of this data (defined by Block.interval_values).
        This are the values as stored in the Block (ndarray or ExtensionArray
        depending on the Block class).

        Differs from the public ``.values`` for certain data types, because of
        historical backwards compatibility of the public attribute (e.g. period
        returns object ndarray and datetimetz a datetime64[ns] ndarray for
        ``.values`` while it returns an ExtensionArray for ``._values`` in those
        cases).

        Differs from ``.array`` in that this still returns the numpy array if
        the Block is backed by a numpy array, while ``.array`` ensures to always
        return an ExtensionArray.

        Differs from ``._ndarray_values``, as that ensures to always return a
        numpy array (it will call ``_ndarray_values`` on the ExtensionArray, if
        the Series was backed by an ExtensionArray).

        Overview:

        dtype       | values        | _values       | array         | _ndarray_values |
        ----------- | ------------- | ------------- | ------------- | --------------- |
        Numeric     | ndarray       | ndarray       | PandasArray   | ndarray         |
        Category    | Categorical   | Categorical   | Categorical   | ndarray[int]    |
        dt64[ns]    | ndarray[M8ns] | ndarray[M8ns] | DatetimeArray | ndarray[M8ns]   |
        dt64[ns tz] | ndarray[M8ns] | DatetimeArray | DatetimeArray | ndarray[M8ns]   |
        Period      | ndarray[obj]  | PeriodArray   | PeriodArray   | ndarray[int]    |
        Nullable    | EA            | EA            | EA            | ndarray         |

        """
        return self._data.internal_values()
