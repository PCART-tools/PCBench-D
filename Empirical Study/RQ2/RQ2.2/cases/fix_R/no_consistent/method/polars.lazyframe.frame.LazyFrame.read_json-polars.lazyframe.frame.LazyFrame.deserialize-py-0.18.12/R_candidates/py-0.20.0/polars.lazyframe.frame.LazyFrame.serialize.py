    def serialize(self, file: IOBase | str | Path | None = None) -> str | None:
        """
        Serialize the logical plan of this LazyFrame to a file or string in JSON format.

        Parameters
        ----------
        file
            File path to which the result should be written. If set to `None`
            (default), the output is returned as a string instead.

        See Also
        --------
        LazyFrame.deserialize

        Examples
        --------
        Serialize the logical plan into a JSON string.

        >>> lf = pl.LazyFrame({"a": [1, 2, 3]}).sum()
        >>> json = lf.serialize()
        >>> json
        '{"Projection":{"expr":[{"Agg":{"Sum":{"Column":"a"}}}],"input":{"DataFrameScan":{"df":{"columns":[{"name":"a","datatype":"Int64","bit_settings":"","values":[1,2,3]}]},"schema":{"inner":{"a":"Int64"}},"output_schema":null,"projection":null,"selection":null}},"schema":{"inner":{"a":"Int64"}},"options":{"run_parallel":true,"duplicate_check":true}}}'

        The logical plan can later be deserialized back into a LazyFrame.

        >>> import io
        >>> pl.LazyFrame.deserialize(io.StringIO(json)).collect()
        shape: (1, 1)
        ┌─────┐
        │ a   │
        │ --- │
        │ i64 │
        ╞═════╡
        │ 6   │
        └─────┘

        """
        if isinstance(file, (str, Path)):
            file = normalize_filepath(file)
        to_string_io = (file is not None) and isinstance(file, StringIO)
        if file is None or to_string_io:
            with BytesIO() as buf:
                self._ldf.serialize(buf)
                json_bytes = buf.getvalue()

            json_str = json_bytes.decode("utf8")
            if to_string_io:
                file.write(json_str)  # type: ignore[union-attr]
            else:
                return json_str
        else:
            self._ldf.serialize(file)
        return None
