    @Appender(fmt.docstring_to_string, indents=1)
    def to_latex(self, buf=None, columns=None, col_space=None, colSpace=None,
                 header=True, index=True, na_rep='NaN', formatters=None,
                 float_format=None, sparsify=None, index_names=True,
                 bold_rows=True, force_unicode=None):
        """
        Render a DataFrame to a tabular environment table.
        You can splice this into a LaTeX document.

        `to_latex`-specific options:

        bold_rows : boolean, default True
            Make the row labels bold in the output

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
                                           header=header, index=index,
                                           formatters=formatters,
                                           float_format=float_format,
                                           bold_rows=bold_rows,
                                           sparsify=sparsify,
                                           index_names=index_names)
        formatter.to_latex()

        if buf is None:
            return formatter.buf.getvalue()
