    @Substitution(buf=buffering_args, encoding=encoding_args)
    def to_html(
        self,
        buf: FilePath | WriteBuffer[str] | None = None,
        *,
        table_uuid: str | None = None,
        table_attributes: str | None = None,
        sparse_index: bool | None = None,
        sparse_columns: bool | None = None,
        bold_headers: bool = False,
        caption: str | None = None,
        max_rows: int | None = None,
        max_columns: int | None = None,
        encoding: str | None = None,
        doctype_html: bool = False,
        exclude_styles: bool = False,
        **kwargs,
    ) -> str | None:
        """
        Write Styler to a file, buffer or string in HTML-CSS format.

        .. versionadded:: 1.3.0

        Parameters
        ----------
        %(buf)s
        table_uuid : str, optional
            Id attribute assigned to the <table> HTML element in the format:

            ``<table id="T_<table_uuid>" ..>``

            If not given uses Styler's initially assigned value.
        table_attributes : str, optional
            Attributes to assign within the `<table>` HTML element in the format:

            ``<table .. <table_attributes> >``

            If not given defaults to Styler's preexisting value.
        sparse_index : bool, optional
            Whether to sparsify the display of a hierarchical index. Setting to False
            will display each explicit level element in a hierarchical key for each row.
            Defaults to ``pandas.options.styler.sparse.index`` value.

            .. versionadded:: 1.4.0
        sparse_columns : bool, optional
            Whether to sparsify the display of a hierarchical index. Setting to False
            will display each explicit level element in a hierarchical key for each
            column. Defaults to ``pandas.options.styler.sparse.columns`` value.

            .. versionadded:: 1.4.0
        bold_headers : bool, optional
            Adds "font-weight: bold;" as a CSS property to table style header cells.

            .. versionadded:: 1.4.0
        caption : str, optional
            Set, or overwrite, the caption on Styler before rendering.

            .. versionadded:: 1.4.0
        max_rows : int, optional
            The maximum number of rows that will be rendered. Defaults to
            ``pandas.options.styler.render.max_rows/max_columns``.

            .. versionadded:: 1.4.0
        max_columns : int, optional
            The maximum number of columns that will be rendered. Defaults to
            ``pandas.options.styler.render.max_columns``, which is None.

            Rows and columns may be reduced if the number of total elements is
            large. This value is set to ``pandas.options.styler.render.max_elements``,
            which is 262144 (18 bit browser rendering).

            .. versionadded:: 1.4.0
        %(encoding)s
        doctype_html : bool, default False
            Whether to output a fully structured HTML file including all
            HTML elements, or just the core ``<style>`` and ``<table>`` elements.
        exclude_styles : bool, default False
            Whether to include the ``<style>`` element and all associated element
            ``class`` and ``id`` identifiers, or solely the ``<table>`` element without
            styling identifiers.
        **kwargs
            Any additional keyword arguments are passed through to the jinja2
            ``self.template.render`` process. This is useful when you need to provide
            additional variables for a custom template.

        Returns
        -------
        str or None
            If `buf` is None, returns the result as a string. Otherwise returns `None`.

        See Also
        --------
        DataFrame.to_html: Write a DataFrame to a file, buffer or string in HTML format.

        Examples
        --------
        >>> df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        >>> print(df.style.to_html())  # doctest: +SKIP
        <style type="text/css">
        </style>
        <table id="T_1e78e">
          <thead>
            <tr>
              <th class="blank level0" >&nbsp;</th>
              <th id="T_1e78e_level0_col0" class="col_heading level0 col0" >A</th>
              <th id="T_1e78e_level0_col1" class="col_heading level0 col1" >B</th>
            </tr>
        ...
        """
        obj = self._copy(deepcopy=True)  # manipulate table_styles on obj, not self

        if table_uuid:
            obj.set_uuid(table_uuid)

        if table_attributes:
            obj.set_table_attributes(table_attributes)

        if sparse_index is None:
            sparse_index = get_option("styler.sparse.index")
        if sparse_columns is None:
            sparse_columns = get_option("styler.sparse.columns")

        if bold_headers:
            obj.set_table_styles(
                [{"selector": "th", "props": "font-weight: bold;"}], overwrite=False
            )

        if caption is not None:
            obj.set_caption(caption)

        # Build HTML string..
        html = obj._render_html(
            sparse_index=sparse_index,
            sparse_columns=sparse_columns,
            max_rows=max_rows,
            max_cols=max_columns,
            exclude_styles=exclude_styles,
            encoding=encoding or get_option("styler.render.encoding"),
            doctype_html=doctype_html,
            **kwargs,
        )

        return save_to_buffer(
            html, buf=buf, encoding=(encoding if buf is not None else None)
        )
