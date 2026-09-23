    def write_json(self, file: IOBase | str | Path | None = None) -> str | None:
        """
        Serialize to JSON representation.

        Parameters
        ----------
        file
            File path or writable file-like object to which the result will be written.
            If set to `None` (default), the output is returned as a string instead.

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
        '[{"foo":1,"bar":6},{"foo":2,"bar":7},{"foo":3,"bar":8}]'
        """

        def write_json_to_string() -> str:
            with BytesIO() as buf:
                self._df.write_json(buf)
                json_bytes = buf.getvalue()
            return json_bytes.decode("utf8")

        if file is None:
            return write_json_to_string()
        elif isinstance(file, StringIO):
            json_str = write_json_to_string()
            file.write(json_str)
            return None
        elif isinstance(file, (str, Path)):
            file = normalize_filepath(file)
            self._df.write_json(file)
            return None
        else:
            self._df.write_json(file)
            return None
