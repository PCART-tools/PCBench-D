    @Appender(fmt.common_docstring + fmt.return_docstring, indents=1)
    def to_latex(self, buf=None, columns=None, col_space=None, header=True,
                 index=True, na_rep='NaN', formatters=None, float_format=None,
                 sparsify=None, index_names=True, bold_rows=True,
                 column_format=None, longtable=None, escape=None,
                 encoding=None, decimal='.'):
        """
        Render a DataFrame to a tabular environment table. You can splice
        this into a LaTeX document. Requires \\usepackage{booktabs}.

        `to_latex`-specific options:

        bold_rows : boolean, default True
            Make the row labels bold in the output
        column_format : str, default None
            The columns format as specified in `LaTeX table format
            <https://en.wikibooks.org/wiki/LaTeX/Tables>`__ e.g 'rcl' for 3
            columns
        longtable : boolean, default will be read from the pandas config module
            default: False
            Use a longtable environment instead of tabular. Requires adding
            a \\usepackage{longtable} to your LaTeX preamble.
        escape : boolean, default will be read from the pandas config module
            default: True
            When set to False prevents from escaping latex special
            characters in column names.
        encoding : str, default None
            A string representing the encoding to use in the output file,
            defaults to 'ascii' on Python 2 and 'utf-8' on Python 3.
        decimal : string, default '.'
            Character recognized as decimal separator, e.g. ',' in Europe

            .. versionadded:: 0.18.0

        """
        # Get defaults from the pandas config
        if longtable is None:
            longtable = get_option("display.latex.longtable")
        if escape is None:
            escape = get_option("display.latex.escape")

        formatter = fmt.DataFrameFormatter(self, buf=buf, columns=columns,
                                           col_space=col_space, na_rep=na_rep,
                                           header=header, index=index,
                                           formatters=formatters,
                                           float_format=float_format,
                                           bold_rows=bold_rows,
                                           sparsify=sparsify,
                                           index_names=index_names,
                                           escape=escape, decimal=decimal)
        formatter.to_latex(column_format=column_format, longtable=longtable,
                           encoding=encoding)

        if buf is None:
            return formatter.buf.getvalue()
