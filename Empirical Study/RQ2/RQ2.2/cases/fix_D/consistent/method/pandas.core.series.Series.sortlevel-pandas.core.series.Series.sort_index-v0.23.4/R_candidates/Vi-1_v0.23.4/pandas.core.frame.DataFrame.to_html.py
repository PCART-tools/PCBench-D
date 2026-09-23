    @Substitution(header='whether to print column labels, default True')
    @Appender(fmt.docstring_to_string, indents=1)
    def to_html(self, buf=None, columns=None, col_space=None, header=True,
                index=True, na_rep='NaN', formatters=None, float_format=None,
                sparsify=None, index_names=True, justify=None, bold_rows=True,
                classes=None, escape=True, max_rows=None, max_cols=None,
                show_dimensions=False, notebook=False, decimal='.',
                border=None, table_id=None):
        """
        Render a DataFrame as an HTML table.

        `to_html`-specific options:

        bold_rows : boolean, default True
            Make the row labels bold in the output
        classes : str or list or tuple, default None
            CSS class(es) to apply to the resulting html table
        escape : boolean, default True
            Convert the characters <, >, and & to HTML-safe sequences.
        max_rows : int, optional
            Maximum number of rows to show before truncating. If None, show
            all.
        max_cols : int, optional
            Maximum number of columns to show before truncating. If None, show
            all.
        decimal : string, default '.'
            Character recognized as decimal separator, e.g. ',' in Europe

            .. versionadded:: 0.18.0

        border : int
            A ``border=border`` attribute is included in the opening
            `<table>` tag. Default ``pd.options.html.border``.

            .. versionadded:: 0.19.0

        table_id : str, optional
            A css id is included in the opening `<table>` tag if specified.

            .. versionadded:: 0.23.0

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
                                           decimal=decimal, table_id=table_id)
        # TODO: a generic formatter wld b in DataFrameFormatter
        formatter.to_html(classes=classes, notebook=notebook, border=border)

        if buf is None:
            return formatter.buf.getvalue()
