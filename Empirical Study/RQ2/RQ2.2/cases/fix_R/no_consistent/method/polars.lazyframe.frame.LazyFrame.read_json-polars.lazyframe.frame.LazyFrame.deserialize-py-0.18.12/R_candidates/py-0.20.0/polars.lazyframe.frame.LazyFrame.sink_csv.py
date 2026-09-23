    @deprecate_renamed_parameter("quote", "quote_char", version="0.19.8")
    @deprecate_renamed_parameter("has_header", "include_header", version="0.19.13")
    def sink_csv(
        self,
        path: str | Path,
        *,
        include_bom: bool = False,
        include_header: bool = True,
        separator: str = ",",
        line_terminator: str = "\n",
        quote_char: str = '"',
        batch_size: int = 1024,
        datetime_format: str | None = None,
        date_format: str | None = None,
        time_format: str | None = None,
        float_precision: int | None = None,
        null_value: str | None = None,
        quote_style: CsvQuoteStyle | None = None,
        maintain_order: bool = True,
        type_coercion: bool = True,
        predicate_pushdown: bool = True,
        projection_pushdown: bool = True,
        simplify_expression: bool = True,
        slice_pushdown: bool = True,
        no_optimization: bool = False,
    ) -> DataFrame:
        """
        Evaluate the query in streaming mode and write to a CSV file.

        This allows streaming results that are larger than RAM to be written to disk.

        Parameters
        ----------
        path
            File path to which the file should be written.
        include_bom
            Whether to include UTF-8 BOM in the CSV output.
        include_header
            Whether to include header in the CSV output.
        separator
            Separate CSV fields with this symbol.
        line_terminator
            String used to end each row.
        quote_char
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
            Number of decimal places to write, applied to both `Float32` and
            `Float64` datatypes.
        null_value
            A string representing null values (defaulting to the empty string).
        quote_style : {'necessary', 'always', 'non_numeric', 'never'}
            Determines the quoting strategy used.

            - necessary (default): This puts quotes around fields only when necessary.
              They are necessary when fields contain a quote,
              delimiter or record terminator.
              Quotes are also necessary when writing an empty record
              (which is indistinguishable from a record with one empty field).
              This is the default.
            - always: This puts quotes around every field. Always.
            - never: This never puts quotes around fields, even if that results in
              invalid CSV data (e.g.: by not quoting strings containing the
              separator).
            - non_numeric: This puts quotes around all fields that are non-numeric.
              Namely, when writing a field that does not parse as a valid float
              or integer, then quotes will be used even if they aren`t strictly
              necessary.
        maintain_order
            Maintain the order in which data is processed.
            Setting this to `False` will  be slightly faster.
        type_coercion
            Do type coercion optimization.
        predicate_pushdown
            Do predicate pushdown optimization.
        projection_pushdown
            Do projection pushdown optimization.
        simplify_expression
            Run simplify expressions optimization.
        slice_pushdown
            Slice pushdown optimization.
        no_optimization
            Turn off (certain) optimizations.

        Returns
        -------
        DataFrame

        Examples
        --------
        >>> lf = pl.scan_csv("/path/to/my_larger_than_ram_file.csv")  # doctest: +SKIP
        >>> lf.sink_csv("out.csv")  # doctest: +SKIP

        """
        _check_arg_is_1byte("separator", separator, can_be_empty=False)
        _check_arg_is_1byte("quote_char", quote_char, can_be_empty=False)
        if not null_value:
            null_value = None

        lf = self._set_sink_optimizations(
            type_coercion=type_coercion,
            predicate_pushdown=predicate_pushdown,
            projection_pushdown=projection_pushdown,
            simplify_expression=simplify_expression,
            slice_pushdown=slice_pushdown,
            no_optimization=no_optimization,
        )

        return lf.sink_csv(
            path=path,
            include_bom=include_bom,
            include_header=include_header,
            separator=ord(separator),
            line_terminator=line_terminator,
            quote_char=ord(quote_char),
            batch_size=batch_size,
            datetime_format=datetime_format,
            date_format=date_format,
            time_format=time_format,
            float_precision=float_precision,
            null_value=null_value,
            quote_style=quote_style,
            maintain_order=maintain_order,
        )
