    @deprecate_renamed_function("json_decode", version="0.19.12")
    def json_extract(
        self, dtype: PolarsDataType | None = None, infer_schema_length: int | None = 100
    ) -> Expr:
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
            How many rows to parse to determine the schema.
            If `None` all rows are used.
        """
        return self.json_decode(dtype, infer_schema_length)
