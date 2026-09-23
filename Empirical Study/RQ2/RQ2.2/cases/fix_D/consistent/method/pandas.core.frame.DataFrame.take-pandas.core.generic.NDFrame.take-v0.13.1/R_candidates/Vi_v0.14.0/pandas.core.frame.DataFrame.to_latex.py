    @Appender(fmt.docstring_to_string, indents=1)
    def to_latex(self, buf=None, columns=None, col_space=None, colSpace=None,
                 header=True, index=True, na_rep='NaN', formatters=None,
                 float_format=None, sparsify=None, index_names=True,
                 bold_rows=True, longtable=False, escape=True):
        """
        Render a DataFrame to a tabular environment table. You can splice
        this into a LaTeX document. Requires \\usepackage(booktabs}.

        `to_latex`-specific options:

        bold_rows : boolean, default True
            Make the row labels bold in the output
        longtable : boolean, default False
            Use a longtable environment instead of tabular. Requires adding
            a \\usepackage{longtable} to your LaTeX preamble.
        escape : boolean, default True
            When set to False prevents from escaping latex special
            characters in column names.

        """

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
                                           index_names=index_names,
                                           escape=escape)
        formatter.to_latex(longtable=longtable)

        if buf is None:
            return formatter.buf.getvalue()
