    @Substitution(header='Whether to print column labels, default True')
    @Substitution(shared_params=fmt.common_docstring,
                  returns=fmt.return_docstring)
    def to_html(self, buf=None, columns=None, col_space=None, header=True,
                index=True, na_rep='NaN', formatters=None, float_format=None,
                sparsify=None, index_names=True, justify=None, max_rows=None,
                max_cols=None, show_dimensions=False, decimal='.',
                bold_rows=True, classes=None, escape=True, notebook=False,
                border=None, table_id=None, render_links=False):
        """
        Render a DataFrame as an HTML table.
        %(shared_params)s
        bold_rows : bool, default True
            Make the row labels bold in the output.
        classes : str or list or tuple, default None
            CSS class(es) to apply to the resulting html table.
        escape : bool, default True
            Convert the characters <, >, and & to HTML-safe sequences.
        notebook : {True, False}, default False
            Whether the generated HTML is for IPython Notebook.
        border : int
            A ``border=border`` attribute is included in the opening
            `<table>` tag. Default ``pd.options.html.border``.

            .. versionadded:: 0.19.0

        table_id : str, optional
            A css id is included in the opening `<table>` tag if specified.

            .. versionadded:: 0.23.0

        render_links : bool, default False
            Convert URLs to HTML links.

            .. versionadded:: 0.24.0

        %(returns)s
        See Also
        --------
        to_string : Convert DataFrame to a string.
        """

        if (justify is not None and
                justify not in fmt._VALID_JUSTIFY_PARAMETERS):
            raise ValueError("Invalid value for justify parameter")

        formatter = fmt.DataFrameFormatter(self, buf=buf, columns=columns,
                                           col_space=col_space, na_rep=na_rep,
                                           formatters=formatters,
                                           float_format=float_format,
                                           sparsify=sparsify, justify=justify,
                                           index_names=index_names,
                                           header=header, index=index,
                                           bold_rows=bold_rows, escape=escape,
                                           max_rows=max_rows,
                                           max_cols=max_cols,
                                           show_dimensions=show_dimensions,
                                           decimal=decimal, table_id=table_id,
                                           render_links=render_links)
        # TODO: a generic formatter wld b in DataFrameFormatter
        formatter.to_html(classes=classes, notebook=notebook, border=border)

        if buf is None:
            return formatter.buf.getvalue()
