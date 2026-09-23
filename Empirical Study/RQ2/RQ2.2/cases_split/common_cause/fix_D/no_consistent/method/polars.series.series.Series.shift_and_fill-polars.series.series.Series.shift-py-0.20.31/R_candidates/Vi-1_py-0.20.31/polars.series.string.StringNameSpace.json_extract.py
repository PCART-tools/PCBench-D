    @deprecate_renamed_function("json_decode", version="0.19.15")
    def json_extract(
        self,
        dtype: PolarsDataType | None = None,
        infer_schema_length: int | None = N_INFER_DEFAULT,
    ) -> Series:
        """
        Parse string values as JSON.

        .. deprecated:: 0.19.15
            This method has been renamed to :meth:`json_decode`.

        Parameters
        ----------
        dtype
            The dtype to cast the extracted value to. If None, the dtype will be
            inferred from the JSON value.
        infer_schema_length
            The maximum number of rows to scan for schema inference.
            If set to `None`, the full data may be scanned *(this is slow)*.
        """
        return self.json_decode(dtype, infer_schema_length)
