    def json_decode(
        self,
        dtype: PolarsDataType | None = None,
        infer_schema_length: int | None = N_INFER_DEFAULT,
    ) -> Series:
        """
        Parse string values as JSON.

        Throws an error if invalid JSON strings are encountered.

        Parameters
        ----------
        dtype
            The dtype to cast the extracted value to. If None, the dtype will be
            inferred from the JSON value.
        infer_schema_length
            The maximum number of rows to scan for schema inference.
            If set to `None`, the full data may be scanned *(this is slow)*.

        See Also
        --------
        json_path_match : Extract the first match of json string with provided JSONPath
            expression.

        Examples
        --------
        >>> s = pl.Series("json", ['{"a":1, "b": true}', None, '{"a":2, "b": false}'])
        >>> s.str.json_decode()
        shape: (3,)
        Series: 'json' [struct[2]]
        [
                {1,true}
                {null,null}
                {2,false}
        ]
        """
