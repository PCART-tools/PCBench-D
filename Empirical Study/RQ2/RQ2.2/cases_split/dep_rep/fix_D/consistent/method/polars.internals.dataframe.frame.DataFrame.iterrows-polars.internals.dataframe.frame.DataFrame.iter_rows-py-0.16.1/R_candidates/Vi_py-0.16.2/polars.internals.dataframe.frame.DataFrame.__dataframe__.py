    def __dataframe__(
        self, nan_as_null: bool = False, allow_copy: bool = True
    ) -> _PyArrowDataFrame:
        """
        Convert to a dataframe object implementing the dataframe interchange protocol.

        Parameters
        ----------
        nan_as_null
            Overwrite null values in the data with ``NaN``.
        allow_copy
            Allow memory to be copied to perform the conversion. If set to False, causes
            conversions that are not zero-copy to fail.

        Notes
        -----
        Details on the dataframe interchange protocol:
        https://data-apis.org/dataframe-protocol/latest/index.html

        `nan_as_null` currently has no effect; once support for nullable extension
        dtypes is added, this value should be propagated to columns.

        """
        if not _PYARROW_AVAILABLE or int(pa.__version__.split(".")[0]) < 11:
            raise ImportError(
                "pyarrow>=11.0.0 is required for converting a Polars dataframe to a"
                " dataframe interchange object."
            )
        if not allow_copy and Categorical in self.schema.values():
            raise NotImplementedError(
                "Polars does not offer zero-copy conversion to Arrow for categorical"
                " columns. Set `allow_copy=True` or cast categorical columns to"
                " string first."
            )
        return self.to_arrow().__dataframe__(nan_as_null, allow_copy)
