    def write_json(
        self,
        file: IOBase | str | Path | None = None,
        pretty: bool = False,
        row_oriented: bool = False,
    ) -> str | None:
        """
        Serialize to JSON representation.

        Parameters
        ----------
        file
            File path to which the result should be written. If set to ``None``
            (default), the output is returned as a string instead.
        pretty
            Pretty serialize json.
        row_oriented
            Write to row oriented json. This is slower, but more common.

        See Also
        --------
        DataFrame.write_ndjson

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [6, 7, 8],
        ...     }
        ... )
        >>> df.write_json()
        '{"columns":[{"name":"foo","datatype":"Int64","values":[1,2,3]},{"name":"bar","datatype":"Int64","values":[6,7,8]}]}'
        >>> df.write_json(row_oriented=True)
        '[{"foo":1,"bar":6},{"foo":2,"bar":7},{"foo":3,"bar":8}]'

        """
        if isinstance(file, (str, Path)):
            file = normalise_filepath(file)
        to_string_io = (file is not None) and isinstance(file, StringIO)
        if file is None or to_string_io:
            with BytesIO() as buf:
                self._df.write_json(buf, pretty, row_oriented)
                json_bytes = buf.getvalue()

            json_str = json_bytes.decode("utf8")
            if to_string_io:
                file.write(json_str)  # type: ignore[union-attr]
            else:
                return json_str
        else:
            self._df.write_json(file, pretty, row_oriented)
        return None
