    @final
    @doc(returns=fmt.return_docstring)
    def to_latex(
        self,
        buf: FilePath | WriteBuffer[str] | None = None,
        columns: Sequence[Hashable] | None = None,
        col_space: ColspaceArgType | None = None,
        header: bool_t | Sequence[str] = True,
        index: bool_t = True,
        na_rep: str = "NaN",
        formatters: FormattersType | None = None,
        float_format: FloatFormatType | None = None,
        sparsify: bool_t | None = None,
        index_names: bool_t = True,
        bold_rows: bool_t = False,
        column_format: str | None = None,
        longtable: bool_t | None = None,
        escape: bool_t | None = None,
        encoding: str | None = None,
        decimal: str = ".",
        multicolumn: bool_t | None = None,
        multicolumn_format: str | None = None,
        multirow: bool_t | None = None,
        caption: str | tuple[str, str] | None = None,
        label: str | None = None,
        position: str | None = None,
    ) -> str | None:
        r"""
        Render object to a LaTeX tabular, longtable, or nested table.

        Requires ``\usepackage{{booktabs}}``.  The output can be copy/pasted
        into a main LaTeX document or read from an external file
        with ``\input{{table.tex}}``.

        .. versionchanged:: 1.0.0
           Added caption and label arguments.

        .. versionchanged:: 1.2.0
           Added position argument, changed meaning of caption argument.

        Parameters
        ----------
        buf : str, Path or StringIO-like, optional, default None
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
        formatters : list of functions or dict of {{str: function}}, optional
            Formatter functions to apply to columns' elements by position or
            name. The result of each function must be a unicode string.
            List must be of length equal to the number of columns.
        float_format : one-parameter function or str, optional, default None
            Formatter for floating point numbers. For example
            ``float_format="%.2f"`` and ``float_format="{{:0.2f}}".format`` will
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
            adding a \usepackage{{longtable}} to your LaTeX preamble.
        escape : bool, optional
            By default, the value will be read from the pandas config
            module. When set to False prevents from escaping latex special
            characters in column names.
        encoding : str, optional
            A string representing the encoding to use in the output file,
            defaults to 'utf-8'.
        decimal : str, default '.'
            Character recognized as decimal separator, e.g. ',' in Europe.
        multicolumn : bool, default True
            Use \multicolumn to enhance MultiIndex columns.
            The default will be read from the config module.
        multicolumn_format : str, default 'l'
            The alignment for multicolumns, similar to `column_format`
            The default will be read from the config module.
        multirow : bool, default False
            Use \multirow to enhance MultiIndex rows. Requires adding a
            \usepackage{{multirow}} to your LaTeX preamble. Will print
            centered labels (instead of top-aligned) across the contained
            rows, separating groups via clines. The default will be read
            from the pandas config module.
        caption : str or tuple, optional
            Tuple (full_caption, short_caption),
            which results in ``\caption[short_caption]{{full_caption}}``;
            if a single string is passed, no short caption will be set.

            .. versionadded:: 1.0.0

            .. versionchanged:: 1.2.0
               Optionally allow caption to be a tuple ``(full_caption, short_caption)``.

        label : str, optional
            The LaTeX label to be placed inside ``\label{{}}`` in the output.
            This is used with ``\ref{{}}`` in the main ``.tex`` file.

            .. versionadded:: 1.0.0
        position : str, optional
            The LaTeX positional argument for tables, to be placed after
            ``\begin{{}}`` in the output.

            .. versionadded:: 1.2.0
        {returns}
        See Also
        --------
        io.formats.style.Styler.to_latex : Render a DataFrame to LaTeX
            with conditional formatting.
        DataFrame.to_string : Render a DataFrame to a console-friendly
            tabular output.
        DataFrame.to_html : Render a DataFrame as an HTML table.

        Examples
        --------
        >>> df = pd.DataFrame(dict(name=['Raphael', 'Donatello'],
        ...                   mask=['red', 'purple'],
        ...                   weapon=['sai', 'bo staff']))
        >>> print(df.to_latex(index=False))  # doctest: +SKIP
        \begin{{tabular}}{{lll}}
         \toprule
               name &    mask &    weapon \\
         \midrule
            Raphael &     red &       sai \\
          Donatello &  purple &  bo staff \\
        \bottomrule
        \end{{tabular}}
        """
        msg = (
            "In future versions `DataFrame.to_latex` is expected to utilise the base "
            "implementation of `Styler.to_latex` for formatting and rendering. "
            "The arguments signature may therefore change. It is recommended instead "
            "to use `DataFrame.style.to_latex` which also contains additional "
            "functionality."
        )
        warnings.warn(
            msg, FutureWarning, stacklevel=find_stack_level(inspect.currentframe())
        )

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

        self = cast("DataFrame", self)
        formatter = DataFrameFormatter(
            self,
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
        return DataFrameRenderer(formatter).to_latex(
            buf=buf,
            column_format=column_format,
            longtable=longtable,
            encoding=encoding,
            multicolumn=multicolumn,
            multicolumn_format=multicolumn_format,
            multirow=multirow,
            caption=caption,
            label=label,
            position=position,
        )
