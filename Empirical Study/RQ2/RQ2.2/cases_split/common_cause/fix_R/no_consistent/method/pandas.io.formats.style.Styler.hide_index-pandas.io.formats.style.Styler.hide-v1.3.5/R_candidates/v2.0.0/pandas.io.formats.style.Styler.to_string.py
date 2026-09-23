    @Substitution(buf=buffering_args, encoding=encoding_args)
    def to_string(
        self,
        buf: FilePath | WriteBuffer[str] | None = None,
        *,
        encoding=None,
        sparse_index: bool | None = None,
        sparse_columns: bool | None = None,
        max_rows: int | None = None,
        max_columns: int | None = None,
        delimiter: str = " ",
    ) -> str | None:
        """
        Write Styler to a file, buffer or string in text format.

        .. versionadded:: 1.5.0

        Parameters
        ----------
        %(buf)s
        %(encoding)s
        sparse_index : bool, optional
            Whether to sparsify the display of a hierarchical index. Setting to False
            will display each explicit level element in a hierarchical key for each row.
            Defaults to ``pandas.options.styler.sparse.index`` value.
        sparse_columns : bool, optional
            Whether to sparsify the display of a hierarchical index. Setting to False
            will display each explicit level element in a hierarchical key for each
            column. Defaults to ``pandas.options.styler.sparse.columns`` value.
        max_rows : int, optional
            The maximum number of rows that will be rendered. Defaults to
            ``pandas.options.styler.render.max_rows``, which is None.
        max_columns : int, optional
            The maximum number of columns that will be rendered. Defaults to
            ``pandas.options.styler.render.max_columns``, which is None.

            Rows and columns may be reduced if the number of total elements is
            large. This value is set to ``pandas.options.styler.render.max_elements``,
            which is 262144 (18 bit browser rendering).
        delimiter : str, default single space
            The separator between data elements.

        Returns
        -------
        str or None
            If `buf` is None, returns the result as a string. Otherwise returns `None`.
        """
        obj = self._copy(deepcopy=True)

        if sparse_index is None:
            sparse_index = get_option("styler.sparse.index")
        if sparse_columns is None:
            sparse_columns = get_option("styler.sparse.columns")

        text = obj._render_string(
            sparse_columns=sparse_columns,
            sparse_index=sparse_index,
            max_rows=max_rows,
            max_cols=max_columns,
            delimiter=delimiter,
        )
        return save_to_buffer(
            text, buf=buf, encoding=(encoding if buf is not None else None)
        )
