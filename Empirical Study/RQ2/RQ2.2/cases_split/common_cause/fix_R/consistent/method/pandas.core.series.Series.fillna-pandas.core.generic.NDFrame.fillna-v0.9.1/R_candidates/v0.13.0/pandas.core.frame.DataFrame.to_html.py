    @Appender(fmt.docstring_to_string, indents=1)
    def to_html(self, buf=None, columns=None, col_space=None, colSpace=None,
                header=True, index=True, na_rep='NaN', formatters=None,
                float_format=None, sparsify=None, index_names=True,
                justify=None, force_unicode=None, bold_rows=True,
                classes=None, escape=True, max_rows=None, max_cols=None,
                show_dimensions=False):
        """
        Render a DataFrame as an HTML table.

        `to_html`-specific options:

        bold_rows : boolean, default True
            Make the row labels bold in the output
        classes : str or list or tuple, default None
            CSS class(es) to apply to the resulting html table
        escape : boolean, default True
            Convert the characters <, >, and & to HTML-safe sequences.=
        max_rows : int, optional
            Maximum number of rows to show before truncating. If None, show
            all.
        max_cols : int, optional
            Maximum number of columns to show before truncating. If None, show
            all.

        """

        if force_unicode is not None:  # pragma: no cover
            warnings.warn("force_unicode is deprecated, it will have no "
                          "effect", FutureWarning)

        if colSpace is not None:  # pragma: no cover
            warnings.warn("colSpace is deprecated, use col_space",
                          FutureWarning)
            col_space = colSpace

        formatter = fmt.DataFrameFormatter(self, buf=buf, columns=columns,
                                           col_space=col_space, na_rep=na_rep,
                                           formatters=formatters,
                                           float_format=float_format,
                                           sparsify=sparsify,
                                           justify=justify,
                                           index_names=index_names,
                                           header=header, index=index,
                                           bold_rows=bold_rows,
                                           escape=escape,
                                           max_rows=max_rows,
                                           max_cols=max_cols,
                                           show_dimensions=show_dimensions)
        formatter.to_html(classes=classes)

        if buf is None:
            return formatter.buf.getvalue()
