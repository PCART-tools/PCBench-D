    @final
    def to_latex(
        self,
        buf: FilePath | WriteBuffer[str] | None = None,
        columns: Sequence[Hashable] | None = None,
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

        .. versionchanged:: 1.2.0
           Added position argument, changed meaning of caption argument.

        .. versionchanged:: 2.0.0
           Refactored to use the Styler implementation via jinja2 templating.

        Parameters
        ----------
        buf : str, Path or StringIO-like, optional, default None
            Buffer to write to. If None, the output is returned as a string.
        columns : list of label, optional
            The subset of columns to write. Writes all columns by default.
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
            Use a longtable environment instead of tabular. Requires
            adding a \usepackage{{longtable}} to your LaTeX preamble.
            By default, the value will be read from the pandas config
            module, and set to `True` if the option ``styler.latex.environment`` is
            `"longtable"`.

            .. versionchanged:: 2.0.0
               The pandas option affecting this argument has changed.
        escape : bool, optional
            By default, the value will be read from the pandas config
            module and set to `True` if the option ``styler.format.escape`` is
            `"latex"`. When set to False prevents from escaping latex special
            characters in column names.

            .. versionchanged:: 2.0.0
               The pandas option affecting this argument has changed, as has the
               default value to `False`.
        encoding : str, optional
            A string representing the encoding to use in the output file,
            defaults to 'utf-8'.
        decimal : str, default '.'
            Character recognized as decimal separator, e.g. ',' in Europe.
        multicolumn : bool, default True
            Use \multicolumn to enhance MultiIndex columns.
            The default will be read from the config module, and is set
            as the option ``styler.sparse.columns``.

            .. versionchanged:: 2.0.0
               The pandas option affecting this argument has changed.
        multicolumn_format : str, default 'r'
            The alignment for multicolumns, similar to `column_format`
            The default will be read from the config module, and is set as the option
            ``styler.latex.multicol_align``.

            .. versionchanged:: 2.0.0
               The pandas option affecting this argument has changed, as has the
               default value to "r".
        multirow : bool, default True
            Use \multirow to enhance MultiIndex rows. Requires adding a
            \usepackage{{multirow}} to your LaTeX preamble. Will print
            centered labels (instead of top-aligned) across the contained
            rows, separating groups via clines. The default will be read
            from the pandas config module, and is set as the option
            ``styler.sparse.index``.

            .. versionchanged:: 2.0.0
               The pandas option affecting this argument has changed, as has the
               default value to `True`.
        caption : str or tuple, optional
            Tuple (full_caption, short_caption),
            which results in ``\caption[short_caption]{{full_caption}}``;
            if a single string is passed, no short caption will be set.

            .. versionchanged:: 1.2.0
               Optionally allow caption to be a tuple ``(full_caption, short_caption)``.

        label : str, optional
            The LaTeX label to be placed inside ``\label{{}}`` in the output.
            This is used with ``\ref{{}}`` in the main ``.tex`` file.

        position : str, optional
            The LaTeX positional argument for tables, to be placed after
            ``\begin{{}}`` in the output.

            .. versionadded:: 1.2.0

        Returns
        -------
        str or None
            If buf is None, returns the result as a string. Otherwise returns None.

        See Also
        --------
        io.formats.style.Styler.to_latex : Render a DataFrame to LaTeX
            with conditional formatting.
        DataFrame.to_string : Render a DataFrame to a console-friendly
            tabular output.
        DataFrame.to_html : Render a DataFrame as an HTML table.

        Notes
        -----
        As of v2.0.0 this method has changed to use the Styler implementation as
        part of :meth:`.Styler.to_latex` via ``jinja2`` templating. This means
        that ``jinja2`` is a requirement, and needs to be installed, for this method
        to function. It is advised that users switch to using Styler, since that
        implementation is more frequently updated and contains much more
        flexibility with the output.

        Examples
        --------
        Convert a general DataFrame to LaTeX with formatting:

        >>> df = pd.DataFrame(dict(name=['Raphael', 'Donatello'],
        ...                        age=[26, 45],
        ...                        height=[181.23, 177.65]))
        >>> print(df.to_latex(index=False,
        ...                   formatters={"name": str.upper},
        ...                   float_format="{:.1f}".format,
        ... ))  # doctest: +SKIP
        \begin{tabular}{lrr}
        \toprule
        name & age & height \\
        \midrule
        RAPHAEL & 26 & 181.2 \\
        DONATELLO & 45 & 177.7 \\
        \bottomrule
        \end{tabular}
        """
        # Get defaults from the pandas config
        if self.ndim == 1:
            self = self.to_frame()
        if longtable is None:
            longtable = config.get_option("styler.latex.environment") == "longtable"
        if escape is None:
            escape = config.get_option("styler.format.escape") == "latex"
        if multicolumn is None:
            multicolumn = config.get_option("styler.sparse.columns")
        if multicolumn_format is None:
            multicolumn_format = config.get_option("styler.latex.multicol_align")
        if multirow is None:
            multirow = config.get_option("styler.sparse.index")

        if column_format is not None and not isinstance(column_format, str):
            raise ValueError("`column_format` must be str or unicode")
        length = len(self.columns) if columns is None else len(columns)
        if isinstance(header, (list, tuple)) and len(header) != length:
            raise ValueError(f"Writing {length} cols but got {len(header)} aliases")

        # Refactor formatters/float_format/decimal/na_rep/escape to Styler structure
        base_format_ = {
            "na_rep": na_rep,
            "escape": "latex" if escape else None,
            "decimal": decimal,
        }
        index_format_: dict[str, Any] = {"axis": 0, **base_format_}
        column_format_: dict[str, Any] = {"axis": 1, **base_format_}

        if isinstance(float_format, str):
            float_format_: Callable | None = lambda x: float_format % x
        else:
            float_format_ = float_format

        def _wrap(x, alt_format_):
            if isinstance(x, (float, complex)) and float_format_ is not None:
                return float_format_(x)
            else:
                return alt_format_(x)

        formatters_: list | tuple | dict | Callable | None = None
        if isinstance(formatters, list):
            formatters_ = {
                c: partial(_wrap, alt_format_=formatters[i])
                for i, c in enumerate(self.columns)
            }
        elif isinstance(formatters, dict):
            index_formatter = formatters.pop("__index__", None)
            column_formatter = formatters.pop("__columns__", None)
            if index_formatter is not None:
                index_format_.update({"formatter": index_formatter})
            if column_formatter is not None:
                column_format_.update({"formatter": column_formatter})

            formatters_ = formatters
            float_columns = self.select_dtypes(include="float").columns
            for col in float_columns:
                if col not in formatters.keys():
                    formatters_.update({col: float_format_})
        elif formatters is None and float_format is not None:
            formatters_ = partial(_wrap, alt_format_=lambda v: v)
        format_index_ = [index_format_, column_format_]

        # Deal with hiding indexes and relabelling column names
        hide_: list[dict] = []
        relabel_index_: list[dict] = []
        if columns:
            hide_.append(
                {
                    "subset": [c for c in self.columns if c not in columns],
                    "axis": "columns",
                }
            )
        if header is False:
            hide_.append({"axis": "columns"})
        elif isinstance(header, (list, tuple)):
            relabel_index_.append({"labels": header, "axis": "columns"})
            format_index_ = [index_format_]  # column_format is overwritten

        if index is False:
            hide_.append({"axis": "index"})
        if index_names is False:
            hide_.append({"names": True, "axis": "index"})

        render_kwargs_ = {
            "hrules": True,
            "sparse_index": sparsify,
            "sparse_columns": sparsify,
            "environment": "longtable" if longtable else None,
            "multicol_align": multicolumn_format
            if multicolumn
            else f"naive-{multicolumn_format}",
            "multirow_align": "t" if multirow else "naive",
            "encoding": encoding,
            "caption": caption,
            "label": label,
            "position": position,
            "column_format": column_format,
            "clines": "skip-last;data"
            if (multirow and isinstance(self.index, MultiIndex))
            else None,
            "bold_rows": bold_rows,
        }

        return self._to_latex_via_styler(
            buf,
            hide=hide_,
            relabel_index=relabel_index_,
            format={"formatter": formatters_, **base_format_},
            format_index=format_index_,
            render_kwargs=render_kwargs_,
        )
