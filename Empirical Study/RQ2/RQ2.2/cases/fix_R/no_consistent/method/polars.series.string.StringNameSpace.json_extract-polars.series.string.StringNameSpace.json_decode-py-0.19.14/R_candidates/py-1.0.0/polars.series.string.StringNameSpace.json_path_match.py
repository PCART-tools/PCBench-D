    def json_path_match(self, json_path: IntoExprColumn) -> Series:
        """
        Extract the first match of json string with provided JSONPath expression.

        Throw errors if encounter invalid json strings.
        All return value will be casted to String regardless of the original value.

        Documentation on JSONPath standard can be found
        `here <https://goessner.net/articles/JsonPath/>`_.

        Parameters
        ----------
        json_path
            A valid JSON path query string.

        Returns
        -------
        Series
            Series of data type :class:`String`. Contains null values if the original
            value is null or the json_path returns nothing.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {"json_val": ['{"a":"1"}', None, '{"a":2}', '{"a":2.1}', '{"a":true}']}
        ... )
        >>> df.select(pl.col("json_val").str.json_path_match("$.a"))[:, 0]
        shape: (5,)
        Series: 'json_val' [str]
        [
            "1"
            null
            "2"
            "2.1"
            "true"
        ]
        """
