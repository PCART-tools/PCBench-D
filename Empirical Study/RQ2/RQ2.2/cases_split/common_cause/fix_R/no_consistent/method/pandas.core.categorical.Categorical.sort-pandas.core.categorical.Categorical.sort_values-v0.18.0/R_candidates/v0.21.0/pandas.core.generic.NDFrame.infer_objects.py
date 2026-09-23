    def infer_objects(self):
        """
        Attempt to infer better dtypes for object columns.

        Attempts soft conversion of object-dtyped
        columns, leaving non-object and unconvertible
        columns unchanged. The inference rules are the
        same as during normal Series/DataFrame construction.

        .. versionadded:: 0.21.0

        See Also
        --------
        pandas.to_datetime : Convert argument to datetime.
        pandas.to_timedelta : Convert argument to timedelta.
        pandas.to_numeric : Convert argument to numeric typeR

        Returns
        -------
        converted : same type as input object

        Examples
        --------
        >>> df = pd.DataFrame({"A": ["a", 1, 2, 3]})
        >>> df = df.iloc[1:]
        >>> df
           A
        1  1
        2  2
        3  3

        >>> df.dtypes
        A    object
        dtype: object

        >>> df.infer_objects().dtypes
        A    int64
        dtype: object
        """
        # numeric=False necessary to only soft convert;
        # python objects will still be converted to
        # native numpy numeric types
        return self._constructor(
            self._data.convert(datetime=True, numeric=False,
                               timedelta=True, coerce=False,
                               copy=True)).__finalize__(self)
