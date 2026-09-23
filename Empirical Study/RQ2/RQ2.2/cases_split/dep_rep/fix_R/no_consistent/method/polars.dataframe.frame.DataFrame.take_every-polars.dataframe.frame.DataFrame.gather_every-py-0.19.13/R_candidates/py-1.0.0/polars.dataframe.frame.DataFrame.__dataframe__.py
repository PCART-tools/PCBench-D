    def __dataframe__(
        self,
        nan_as_null: bool = False,  # noqa: FBT001
        allow_copy: bool = True,  # noqa: FBT001
    ) -> PolarsDataFrame:
        """
        Convert to a dataframe object implementing the dataframe interchange protocol.

        Parameters
        ----------
        nan_as_null
            Overwrite null values in the data with `NaN`.

            .. warning::
                This functionality has not been implemented and the parameter will be
                removed in a future version.
                Setting this to `True` will raise a `NotImplementedError`.
        allow_copy
            Allow memory to be copied to perform the conversion. If set to `False`,
            causes conversions that are not zero-copy to fail.

        Notes
        -----
        Details on the Python dataframe interchange protocol:
        https://data-apis.org/dataframe-protocol/latest/index.html

        Examples
        --------
        Convert a Polars DataFrame to a generic dataframe object and access some
        properties.

        >>> df = pl.DataFrame({"a": [1, 2], "b": [3.0, 4.0], "c": ["x", "y"]})
        >>> dfi = df.__dataframe__()
        >>> dfi.num_rows()
        2
        >>> dfi.get_column(1).dtype
        (<DtypeKind.FLOAT: 2>, 64, 'g', '=')
        """
        if nan_as_null:
            msg = (
                "functionality for `nan_as_null` has not been implemented and the"
                " parameter will be removed in a future version"
                "\n\nUse the default `nan_as_null=False`."
            )
            raise NotImplementedError(msg)

        from polars.interchange.dataframe import PolarsDataFrame

        return PolarsDataFrame(self, allow_copy=allow_copy)
