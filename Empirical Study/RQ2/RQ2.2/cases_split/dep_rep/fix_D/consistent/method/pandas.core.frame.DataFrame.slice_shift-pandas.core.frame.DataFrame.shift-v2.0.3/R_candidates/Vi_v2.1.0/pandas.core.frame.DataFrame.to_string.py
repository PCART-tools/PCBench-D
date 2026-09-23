    @Substitution(
        header_type="bool or list of str",
        header="Write out the column names. If a list of columns "
        "is given, it is assumed to be aliases for the "
        "column names",
        col_space_type="int, list or dict of int",
        col_space="The minimum width of each column. If a list of ints is given "
        "every integers corresponds with one column. If a dict is given, the key "
        "references the column, while the value defines the space to use.",
    )
    @Substitution(shared_params=fmt.common_docstring, returns=fmt.return_docstring)
    def to_string(
        self,
        buf: FilePath | WriteBuffer[str] | None = None,
        columns: Axes | None = None,
        col_space: int | list[int] | dict[Hashable, int] | None = None,
        header: bool | list[str] = True,
        index: bool = True,
        na_rep: str = "NaN",
        formatters: fmt.FormattersType | None = None,
        float_format: fmt.FloatFormatType | None = None,
        sparsify: bool | None = None,
        index_names: bool = True,
        justify: str | None = None,
        max_rows: int | None = None,
        max_cols: int | None = None,
        show_dimensions: bool = False,
        decimal: str = ".",
        line_width: int | None = None,
        min_rows: int | None = None,
        max_colwidth: int | None = None,
        encoding: str | None = None,
    ) -> str | None:
        """
        Render a DataFrame to a console-friendly tabular output.
        %(shared_params)s
        line_width : int, optional
            Width to wrap a line in characters.
        min_rows : int, optional
            The number of rows to display in the console in a truncated repr
            (when number of rows is above `max_rows`).
        max_colwidth : int, optional
            Max width to truncate each column in characters. By default, no limit.
        encoding : str, default "utf-8"
            Set character encoding.
        %(returns)s
        See Also
        --------
        to_html : Convert DataFrame to HTML.

        Examples
        --------
        >>> d = {'col1': [1, 2, 3], 'col2': [4, 5, 6]}
        >>> df = pd.DataFrame(d)
        >>> print(df.to_string())
           col1  col2
        0     1     4
        1     2     5
        2     3     6
        """
        from pandas import option_context

        with option_context("display.max_colwidth", max_colwidth):
            formatter = fmt.DataFrameFormatter(
                self,
                columns=columns,
                col_space=col_space,
                na_rep=na_rep,
                formatters=formatters,
                float_format=float_format,
                sparsify=sparsify,
                justify=justify,
                index_names=index_names,
                header=header,
                index=index,
                min_rows=min_rows,
                max_rows=max_rows,
                max_cols=max_cols,
                show_dimensions=show_dimensions,
                decimal=decimal,
            )
            return fmt.DataFrameRenderer(formatter).to_string(
                buf=buf,
                encoding=encoding,
                line_width=line_width,
            )
