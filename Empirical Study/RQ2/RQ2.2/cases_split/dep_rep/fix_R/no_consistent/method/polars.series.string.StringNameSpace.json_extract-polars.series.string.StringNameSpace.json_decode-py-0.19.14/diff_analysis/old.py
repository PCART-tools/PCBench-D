    def json_extract(
        self, dtype: PolarsDataType | None = None, infer_schema_length: int | None = 100
    ) -> Series:
        """
        Parse string values as JSON.

        Throw errors if encounter invalid JSON strings.

        Parameters
        ----------
        dtype
            The dtype to cast the extracted value to. If None, the dtype will be
            inferred from the JSON value.
        infer_schema_length
            How many rows to parse to determine the schema.
            If `None` all rows are used.

        See Also
        --------
        json_path_match : Extract the first match of json string with provided JSONPath
            expression.

        Examples
        --------
        >>> s = pl.Series("json", ['{"a":1, "b": true}', None, '{"a":2, "b": false}'])
        >>> s.str.json_extract()
        shape: (3,)
        Series: 'json' [struct[2]]
        [
                {1,true}
                {null,null}
                {2,false}
        ]

        """
