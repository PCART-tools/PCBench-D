    @final
    def infer_objects(self: NDFrameT, copy: bool_t | None = None) -> NDFrameT:
        """
        Attempt to infer better dtypes for object columns.

        Attempts soft conversion of object-dtyped
        columns, leaving non-object and unconvertible
        columns unchanged. The inference rules are the
        same as during normal Series/DataFrame construction.

        Parameters
        ----------
        copy : bool, default True
            Whether to make a copy for non-object or non-inferrable columns
            or Series.

        Returns
        -------
        same type as input object

        See Also
        --------
        to_datetime : Convert argument to datetime.
        to_timedelta : Convert argument to timedelta.
        to_numeric : Convert argument to numeric type.
        convert_dtypes : Convert argument to best possible dtype.

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
        new_mgr = self._mgr.convert(copy=copy)
        return self._constructor(new_mgr).__finalize__(self, method="infer_objects")
