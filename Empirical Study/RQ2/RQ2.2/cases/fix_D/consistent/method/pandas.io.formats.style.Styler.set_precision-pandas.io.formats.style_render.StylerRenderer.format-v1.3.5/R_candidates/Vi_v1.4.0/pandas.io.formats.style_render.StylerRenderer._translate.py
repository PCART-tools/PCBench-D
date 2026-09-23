    def _translate(
        self,
        sparse_index: bool,
        sparse_cols: bool,
        max_rows: int | None = None,
        max_cols: int | None = None,
        blank: str = "&nbsp;",
    ):
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
        blank : str
            Entry to top-left blank cells.
        max_rows, max_cols : int, optional
            Specific max rows and cols. max_elements always take precedence in render.

        Returns
        -------
        d : dict
            The following structure: {uuid, table_styles, caption, head, body,
            cellstyle, table_attributes}
        """
        self.css["blank_value"] = blank

        # construct render dict
        d = {
            "uuid": self.uuid,
            "table_styles": format_table_styles(self.table_styles or []),
            "caption": self.caption,
        }

        max_elements = get_option("styler.render.max_elements")
        max_rows = max_rows if max_rows else get_option("styler.render.max_rows")
        max_cols = max_cols if max_cols else get_option("styler.render.max_columns")
        max_rows, max_cols = _get_trimming_maximums(
            len(self.data.index),
            len(self.data.columns),
            max_elements,
            max_rows,
            max_cols,
        )

        self.cellstyle_map_columns: DefaultDict[
            tuple[CSSPair, ...], list[str]
        ] = defaultdict(list)
        head = self._translate_header(sparse_cols, max_cols)
        d.update({"head": head})

        # for sparsifying a MultiIndex and for use with latex clines
        idx_lengths = _get_level_lengths(
            self.index, sparse_index, max_rows, self.hidden_rows
        )
        d.update({"index_lengths": idx_lengths})

        self.cellstyle_map: DefaultDict[tuple[CSSPair, ...], list[str]] = defaultdict(
            list
        )
        self.cellstyle_map_index: DefaultDict[
            tuple[CSSPair, ...], list[str]
        ] = defaultdict(list)
        body = self._translate_body(idx_lengths, max_rows, max_cols)
        d.update({"body": body})

        ctx_maps = {
            "cellstyle": "cellstyle_map",
            "cellstyle_index": "cellstyle_map_index",
            "cellstyle_columns": "cellstyle_map_columns",
        }  # add the cell_ids styles map to the render dictionary in right format
        for k, attr in ctx_maps.items():
            map = [
                {"props": list(props), "selectors": selectors}
                for props, selectors in getattr(self, attr).items()
            ]
            d.update({k: map})

        table_attr = self.table_attributes
        if not get_option("styler.html.mathjax"):
            table_attr = table_attr or ""
            if 'class="' in table_attr:
                table_attr = table_attr.replace('class="', 'class="tex2jax_ignore ')
            else:
                table_attr += ' class="tex2jax_ignore"'
        d.update({"table_attributes": table_attr})

        if self.tooltips:
            d = self.tooltips._translate(self, d)

        return d
