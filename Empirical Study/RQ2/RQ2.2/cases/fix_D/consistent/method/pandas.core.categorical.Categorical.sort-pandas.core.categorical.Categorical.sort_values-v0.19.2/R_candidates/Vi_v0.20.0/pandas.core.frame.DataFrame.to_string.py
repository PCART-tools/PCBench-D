    @Substitution(header='Write out column names. If a list of string is given, \
it is assumed to be aliases for the column names')
    @Appender(fmt.docstring_to_string, indents=1)
    def to_string(self, buf=None, columns=None, col_space=None, header=True,
                  index=True, na_rep='NaN', formatters=None, float_format=None,
                  sparsify=None, index_names=True, justify=None,
                  line_width=None, max_rows=None, max_cols=None,
                  show_dimensions=False):
        """
        Render a DataFrame to a console-friendly tabular output.
        """

        formatter = fmt.DataFrameFormatter(self, buf=buf, columns=columns,
                                           col_space=col_space, na_rep=na_rep,
                                           formatters=formatters,
                                           float_format=float_format,
                                           sparsify=sparsify, justify=justify,
                                           index_names=index_names,
                                           header=header, index=index,
                                           line_width=line_width,
                                           max_rows=max_rows,
                                           max_cols=max_cols,
                                           show_dimensions=show_dimensions)
        formatter.to_string()

        if buf is None:
            result = formatter.buf.getvalue()
            return result
