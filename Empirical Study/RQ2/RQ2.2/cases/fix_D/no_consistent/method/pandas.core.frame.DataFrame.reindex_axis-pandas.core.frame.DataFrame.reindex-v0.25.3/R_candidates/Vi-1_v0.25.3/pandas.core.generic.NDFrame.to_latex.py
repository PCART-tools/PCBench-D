    def to_latex(
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
        bold_rows=False,
        column_format=None,
        longtable=None,
        escape=None,
        encoding=None,
        decimal=".",
        multicolumn=None,
        multicolumn_format=None,
        multirow=None,
    ):
        r"""
        Render an object to a LaTeX tabular environment table.

        Render an object to a tabular environment table. You can splice
        this into a LaTeX document. Requires \usepackage{booktabs}.

        .. versionchanged:: 0.20.2
           Added to Series

        Parameters
        ----------
        buf : file descriptor or None
            Buffer to write to. If None, the output is returned as a string.
        columns : list of label, optional
            The subset of columns to write. Writes all columns by default.
        col_space : int, optional
            The minimum width of each column.
        header : bool or list of str, default True
            Write out the column names. If a list of strings is given,
            it is assumed to be aliases for the column names.
        index : bool, default True
            Write row names (index).
        na_rep : str, default 'NaN'
            Missing data representation.
        formatters : list of functions or dict of {str: function}, optional
            Formatter functions to apply to columns' elements by position or
            name. The result of each function must be a unicode string.
            List must be of length equal to the number of columns.
        float_format : one-parameter function or str, optional, default None
            Formatter for floating point numbers. For example
            ``float_format="%%.2f"`` and ``float_format="{:0.2f}".format`` will
            both result in 0.1234 being formatted as 0.12.
        sparsify : bool, optional
            Set to False for a DataFrame with a hierarchical index to print
            every multiindex key at each row. By default, the value will be
            read from the config module.
        index_names : bool, default True
            Prints the names of the indexes.
        bold_rows : bool, default False
            Make the row labels bold in the output.
        column_format : str, optional
            The columns format as specified in `LaTeX table format
            <https://en.wikibooks.org/wiki/LaTeX/Tables>`__ e.g. 'rcl' for 3
            columns. By default, 'l' will be used for all columns except
            columns of numbers, which default to 'r'.
        longtable : bool, optional
            By default, the value will be read from the pandas config
            module. Use a longtable environment instead of tabular. Requires
            adding a \usepackage{longtable} to your LaTeX preamble.
        escape : bool, optional
            By default, the value will be read from the pandas config
            module. When set to False prevents from escaping latex special
            characters in column names.
        encoding : str, optional
            A string representing the encoding to use in the output file,
            defaults to 'utf-8'.
        decimal : str, default '.'
            Character recognized as decimal separator, e.g. ',' in Europe.

            .. versionadded:: 0.18.0
        multicolumn : bool, default True
            Use \multicolumn to enhance MultiIndex columns.
            The default will be read from the config module.

            .. versionadded:: 0.20.0
        multicolumn_format : str, default 'l'
            The alignment for multicolumns, similar to `column_format`
            The default will be read from the config module.

            .. versionadded:: 0.20.0
        multirow : bool, default False
            Use \multirow to enhance MultiIndex rows. Requires adding a
            \usepackage{multirow} to your LaTeX preamble. Will print
            centered labels (instead of top-aligned) across the contained
            rows, separating groups via clines. The default will be read
            from the pandas config module.

            .. versionadded:: 0.20.0

        Returns
        -------
        str or None
            If buf is None, returns the resulting LateX format as a
            string. Otherwise returns None.

        See Also
        --------
        DataFrame.to_string : Render a DataFrame to a console-friendly
            tabular output.
        DataFrame.to_html : Render a DataFrame as an HTML table.

        Examples
        --------
        >>> df = pd.DataFrame({'name': ['Raphael', 'Donatello'],
        ...                    'mask': ['red', 'purple'],
        ...                    'weapon': ['sai', 'bo staff']})
        >>> df.to_latex(index=False) # doctest: +NORMALIZE_WHITESPACE
        '\\begin{tabular}{lll}\n\\toprule\n      name &    mask &    weapon
        \\\\\n\\midrule\n   Raphael &     red &       sai \\\\\n Donatello &
         purple &  bo staff \\\\\n\\bottomrule\n\\end{tabular}\n'
        """
        # Get defaults from the pandas config
        if self.ndim == 1:
            self = self.to_frame()
        if longtable is None:
            longtable = config.get_option("display.latex.longtable")
        if escape is None:
            escape = config.get_option("display.latex.escape")
        if multicolumn is None:
            multicolumn = config.get_option("display.latex.multicolumn")
        if multicolumn_format is None:
            multicolumn_format = config.get_option("display.latex.multicolumn_format")
        if multirow is None:
            multirow = config.get_option("display.latex.multirow")

        formatter = DataFrameFormatter(
            self,
            buf=buf,
            columns=columns,
            col_space=col_space,
            na_rep=na_rep,
            header=header,
            index=index,
            formatters=formatters,
            float_format=float_format,
            bold_rows=bold_rows,
            sparsify=sparsify,
            index_names=index_names,
            escape=escape,
            decimal=decimal,
        )
        formatter.to_latex(
            column_format=column_format,
            longtable=longtable,
            encoding=encoding,
            multicolumn=multicolumn,
            multicolumn_format=multicolumn_format,
            multirow=multirow,
        )

        if buf is None:
            return formatter.buf.getvalue()
