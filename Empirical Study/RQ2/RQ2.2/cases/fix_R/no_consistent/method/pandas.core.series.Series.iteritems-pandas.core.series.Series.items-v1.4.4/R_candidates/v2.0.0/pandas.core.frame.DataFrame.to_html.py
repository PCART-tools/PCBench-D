    @Substitution(
        header_type="bool",
        header="Whether to print column labels, default True",
        col_space_type="str or int, list or dict of int or str",
        col_space="The minimum width of each column in CSS length "
        "units.  An int is assumed to be px units.",
    )
    @Substitution(shared_params=fmt.common_docstring, returns=fmt.return_docstring)
    def to_html(
        self,
        buf: FilePath | WriteBuffer[str] | None = None,
        columns: Sequence[Level] | None = None,
        col_space: ColspaceArgType | None = None,
        header: bool | Sequence[str] = True,
        index: bool = True,
        na_rep: str = "NaN",
        formatters: FormattersType | None = None,
        float_format: FloatFormatType | None = None,
        sparsify: bool | None = None,
        index_names: bool = True,
        justify: str | None = None,
        max_rows: int | None = None,
        max_cols: int | None = None,
        show_dimensions: bool | str = False,
        decimal: str = ".",
        bold_rows: bool = True,
        classes: str | list | tuple | None = None,
        escape: bool = True,
        notebook: bool = False,
        border: int | bool | None = None,
        table_id: str | None = None,
        render_links: bool = False,
        encoding: str | None = None,
    ) -> str | None:
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
            `<table>` tag. Default ``pd.options.display.html.border``.
        table_id : str, optional
            A css id is included in the opening `<table>` tag if specified.
        render_links : bool, default False
            Convert URLs to HTML links.
        encoding : str, default "utf-8"
            Set character encoding.

            .. versionadded:: 1.0
        %(returns)s
        See Also
        --------
        to_string : Convert DataFrame to a string.
        """
        if justify is not None and justify not in fmt._VALID_JUSTIFY_PARAMETERS:
            raise ValueError("Invalid value for justify parameter")

        formatter = fmt.DataFrameFormatter(
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
            justify=justify,
            index_names=index_names,
            escape=escape,
            decimal=decimal,
            max_rows=max_rows,
            max_cols=max_cols,
            show_dimensions=show_dimensions,
        )
        # TODO: a generic formatter wld b in DataFrameFormatter
        return fmt.DataFrameRenderer(formatter).to_html(
            buf=buf,
            classes=classes,
            notebook=notebook,
            border=border,
            encoding=encoding,
            table_id=table_id,
            render_links=render_links,
        )
