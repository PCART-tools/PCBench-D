    @Substitution(
        header="Write out the column names. If a list of strings "
        "is given, it is assumed to be aliases for the "
        "column names",
        col_space_type="int",
        col_space="The minimum width of each column",
    )
    @Substitution(shared_params=fmt.common_docstring, returns=fmt.return_docstring)
    def to_string(
        self,
        buf=None,
        columns=None,
        col_space=None,
        header=True,
        index=True,
        na_rep="NaN",
        formatters=None,
        float_format=None,
        sparsify=None,
        index_names=True,
        justify=None,
        max_rows=None,
        min_rows=None,
        max_cols=None,
        show_dimensions=False,
        decimal=".",
        line_width=None,
    ):
        """
        Render a DataFrame to a console-friendly tabular output.
        %(shared_params)s
        line_width : int, optional
            Width to wrap a line in characters.
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

        formatter = fmt.DataFrameFormatter(
            self,
            buf=buf,
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
        formatter.to_string()

        if buf is None:
            result = formatter.buf.getvalue()
            return result
