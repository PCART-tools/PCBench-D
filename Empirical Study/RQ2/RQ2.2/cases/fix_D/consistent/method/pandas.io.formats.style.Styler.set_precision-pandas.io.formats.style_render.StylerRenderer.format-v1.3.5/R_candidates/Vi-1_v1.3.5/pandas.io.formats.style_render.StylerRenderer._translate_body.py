    def _translate_body(
        self,
        data_class: str,
        row_heading_class: str,
        sparsify_index: bool,
        max_rows: int,
        max_cols: int,
        trimmed_row_class: str,
        trimmed_col_class: str,
    ):
        """
        Build each <tr> within table <body> as a list

        Use the following structure:
          +--------------------------------------------+---------------------------+
          |  index_header_0    ...    index_header_n   |  data_by_column           |
          +--------------------------------------------+---------------------------+

        Also add elements to the cellstyle_map for more efficient grouped elements in
        <style></style> block

        Parameters
        ----------
        data_class : str
            CSS class added to elements within data_by_column sections of the structure.
        row_heading_class : str
            CSS class added to elements within the index_header section of structure.
        sparsify_index : bool
            Whether index_headers section will add rowspan attributes (>1) to elements.

        Returns
        -------
        body : list
            The associated HTML elements needed for template rendering.
        """
        # for sparsifying a MultiIndex
        idx_lengths = _get_level_lengths(
            self.index, sparsify_index, max_rows, self.hidden_rows
        )

        rlabels = self.data.index.tolist()[:max_rows]  # slice to allow trimming
        if self.data.index.nlevels == 1:
            rlabels = [[x] for x in rlabels]

        body = []
        for r, row_tup in enumerate(self.data.itertuples()):
            if r >= max_rows:  # used only to add a '...' trimmed row:
                index_headers = [
                    _element(
                        "th",
                        f"{row_heading_class} level{c} {trimmed_row_class}",
                        "...",
                        not self.hide_index_,
                        attributes="",
                    )
                    for c in range(self.data.index.nlevels)
                ]

                data = [
                    _element(
                        "td",
                        f"{data_class} col{c} {trimmed_row_class}",
                        "...",
                        (c not in self.hidden_columns),
                        attributes="",
                    )
                    for c in range(max_cols)
                ]

                if len(self.data.columns) > max_cols:
                    # columns are also trimmed so we add the final element
                    data.append(
                        _element(
                            "td",
                            f"{data_class} {trimmed_row_class} {trimmed_col_class}",
                            "...",
                            True,
                            attributes="",
                        )
                    )

                body.append(index_headers + data)
                break

            index_headers = [
                _element(
                    "th",
                    f"{row_heading_class} level{c} row{r}",
                    value,
                    (_is_visible(r, c, idx_lengths) and not self.hide_index_),
                    id=f"level{c}_row{r}",
                    attributes=(
                        f'rowspan="{idx_lengths.get((c, r), 0)}"'
                        if idx_lengths.get((c, r), 0) > 1
                        else ""
                    ),
                )
                for c, value in enumerate(rlabels[r])
            ]

            data = []
            for c, value in enumerate(row_tup[1:]):
                if c >= max_cols:
                    data.append(
                        _element(
                            "td",
                            f"{data_class} row{r} {trimmed_col_class}",
                            "...",
                            True,
                            attributes="",
                        )
                    )
                    break

                # add custom classes from cell context
                cls = ""
                if (r, c) in self.cell_context:
                    cls = " " + self.cell_context[r, c]

                data_element = _element(
                    "td",
                    f"{data_class} row{r} col{c}{cls}",
                    value,
                    (c not in self.hidden_columns and r not in self.hidden_rows),
                    attributes="",
                    display_value=self._display_funcs[(r, c)](value),
                )

                # only add an id if the cell has a style
                if self.cell_ids or (r, c) in self.ctx:
                    data_element["id"] = f"row{r}_col{c}"
                    if (r, c) in self.ctx and self.ctx[r, c]:  # only add  if non-empty
                        self.cellstyle_map[tuple(self.ctx[r, c])].append(
                            f"row{r}_col{c}"
                        )

                data.append(data_element)

            body.append(index_headers + data)
        return body
