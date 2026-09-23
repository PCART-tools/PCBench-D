    def write_csv(
        self,
        file: BytesIO | str | Path | None = None,
        has_header: bool = True,
        sep: str = ",",
        quote: str = '"',
        batch_size: int = 1024,
        datetime_format: str | None = None,
        date_format: str | None = None,
        time_format: str | None = None,
        float_precision: int | None = None,
        null_value: str | None = None,
    ) -> str | None:
        """
        Write to comma-separated values (CSV) file.

        Parameters
        ----------
        file
            File path to which the result should be written. If set to ``None``
            (default), the output is returned as a string instead.
        has_header
            Whether to include header in the CSV output.
        sep
            Separate CSV fields with this symbol.
        quote
            Byte to use as quoting character.
        batch_size
            Number of rows that will be processed per thread.
        datetime_format
            A format string, with the specifiers defined by the
            `chrono <https://docs.rs/chrono/latest/chrono/format/strftime/index.html>`_
            Rust crate. If no format specified, the default fractional-second
            precision is inferred from the maximum timeunit found in the frame's
            Datetime cols (if any).
        date_format
            A format string, with the specifiers defined by the
            `chrono <https://docs.rs/chrono/latest/chrono/format/strftime/index.html>`_
            Rust crate.
        time_format
            A format string, with the specifiers defined by the
            `chrono <https://docs.rs/chrono/latest/chrono/format/strftime/index.html>`_
            Rust crate.
        float_precision
            Number of decimal places to write, applied to both ``Float32`` and
            ``Float64`` datatypes.
        null_value
            A string representing null values (defaulting to the empty string).

        Examples
        --------
        >>> import pathlib
        >>>
        >>> df = pl.DataFrame(
        ...     {
        ...         "foo": [1, 2, 3, 4, 5],
        ...         "bar": [6, 7, 8, 9, 10],
        ...         "ham": ["a", "b", "c", "d", "e"],
        ...     }
        ... )
        >>> path: pathlib.Path = dirpath / "new_file.csv"
        >>> df.write_csv(path, sep=",")

        """
        if len(sep) > 1:
            raise ValueError("only single byte separator is allowed")
        elif len(quote) > 1:
            raise ValueError("only single byte quote char is allowed")
        elif null_value == "":
            null_value = None

        if file is None:
            buffer = BytesIO()
            self._df.write_csv(
                buffer,
                has_header,
                ord(sep),
                ord(quote),
                batch_size,
                datetime_format,
                date_format,
                time_format,
                float_precision,
                null_value,
            )
            return str(buffer.getvalue(), encoding="utf-8")

        if isinstance(file, (str, Path)):
            file = normalise_filepath(file)

        self._df.write_csv(
            file,
            has_header,
            ord(sep),
            ord(quote),
            batch_size,
            datetime_format,
            date_format,
            time_format,
            float_precision,
            null_value,
        )
        return None
