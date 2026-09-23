    def _translate(self, sparse_index: bool, sparse_cols: bool, blank: str = "&nbsp;"):
        """
        Process Styler data and settings into a dict for template rendering.

        Convert data and settings from ``Styler`` attributes such as ``self.data``,
        ``self.tooltips`` including applying any methods in ``self._todo``.

        Parameters
        ----------
        sparse_index : bool
            Whether to sparsify the index or print all hierarchical index elements.
            Upstream defaults are typically to `pandas.options.styler.sparse.index`.
        sparse_cols : bool
            Whether to sparsify the columns or print all hierarchical column elements.
            Upstream defaults are typically to `pandas.options.styler.sparse.columns`.

        Returns
        -------
        d : dict
            The following structure: {uuid, table_styles, caption, head, body,
            cellstyle, table_attributes}
        """
        ROW_HEADING_CLASS = "row_heading"
        COL_HEADING_CLASS = "col_heading"
        INDEX_NAME_CLASS = "index_name"
        TRIMMED_COL_CLASS = "col_trim"
        TRIMMED_ROW_CLASS = "row_trim"

        DATA_CLASS = "data"
        BLANK_CLASS = "blank"
        BLANK_VALUE = blank

        # construct render dict
        d = {
            "uuid": self.uuid,
            "table_styles": _format_table_styles(self.table_styles or []),
            "caption": self.caption,
        }

        max_elements = get_option("styler.render.max_elements")
        max_rows, max_cols = _get_trimming_maximums(
            len(self.data.index), len(self.data.columns), max_elements
        )

        head = self._translate_header(
            BLANK_CLASS,
            BLANK_VALUE,
            INDEX_NAME_CLASS,
            COL_HEADING_CLASS,
            sparse_cols,
            max_cols,
            TRIMMED_COL_CLASS,
        )
        d.update({"head": head})

        self.cellstyle_map: DefaultDict[tuple[CSSPair, ...], list[str]] = defaultdict(
            list
        )
        body = self._translate_body(
            DATA_CLASS,
            ROW_HEADING_CLASS,
            sparse_index,
            max_rows,
            max_cols,
            TRIMMED_ROW_CLASS,
            TRIMMED_COL_CLASS,
        )
        d.update({"body": body})

        cellstyle: list[dict[str, CSSList | list[str]]] = [
            {"props": list(props), "selectors": selectors}
            for props, selectors in self.cellstyle_map.items()
        ]
        d.update({"cellstyle": cellstyle})

        table_attr = self.table_attributes
        use_mathjax = get_option("display.html.use_mathjax")
        if not use_mathjax:
            table_attr = table_attr or ""
            if 'class="' in table_attr:
                table_attr = table_attr.replace('class="', 'class="tex2jax_ignore ')
            else:
                table_attr += ' class="tex2jax_ignore"'
        d.update({"table_attributes": table_attr})

        if self.tooltips:
            d = self.tooltips._translate(self.data, self.uuid, d)

        return d
