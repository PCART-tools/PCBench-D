    @Substitution(
        header_type="bool or sequence",
        header="Write out the column names. If a list of strings "
        "is given, it is assumed to be aliases for the "
        "column names",
        col_space_type="int",
        col_space="The minimum width of each column",
    )
    @Substitution(shared_params=fmt.common_docstring, returns=fmt.return_docstring)
    def to_string(
        self,
        buf: Optional[FilePathOrBuffer[str]] = None,
        columns: Optional[Sequence[str]] = None,
        col_space: Optional[int] = None,
        header: Union[bool, Sequence[str]] = True,
        index: bool = True,
        na_rep: str = "NaN",
        formatters: Optional[fmt.formatters_type] = None,
        float_format: Optional[fmt.float_format_type] = None,
        sparsify: Optional[bool] = None,
        index_names: bool = True,
        justify: Optional[str] = None,
        max_rows: Optional[int] = None,
        min_rows: Optional[int] = None,
        max_cols: Optional[int] = None,
        show_dimensions: bool = False,
        decimal: str = ".",
        line_width: Optional[int] = None,
        max_colwidth: Optional[int] = None,
        encoding: Optional[str] = None,
    ) -> Optional[str]:
        """
        Render a DataFrame to a console-friendly tabular output.
        %(shared_params)s
        line_width : int, optional
            Width to wrap a line in characters.
        max_colwidth : int, optional
            Max width to truncate each column in characters. By default, no limit.

            .. versionadded:: 1.0.0
        encoding : str, default "utf-8"
            Set character encoding.

            .. versionadded:: 1.0
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
                line_width=line_width,
            )
            return formatter.to_string(buf=buf, encoding=encoding)
