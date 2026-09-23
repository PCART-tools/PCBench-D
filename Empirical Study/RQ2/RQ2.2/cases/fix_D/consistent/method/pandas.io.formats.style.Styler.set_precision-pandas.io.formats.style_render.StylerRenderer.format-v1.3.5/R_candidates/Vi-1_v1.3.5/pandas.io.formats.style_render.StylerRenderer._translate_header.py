    def _translate_header(
        self,
        blank_class: str,
        blank_value: str,
        index_name_class: str,
        col_heading_class: str,
        sparsify_cols: bool,
        max_cols: int,
        trimmed_col_class: str,
    ):
        """
        Build each <tr> within table <head> as a list

        Using the structure:
             +----------------------------+---------------+---------------------------+
             |  index_blanks ...          | column_name_0 |  column_headers (level_0) |
          1) |       ..                   |       ..      |             ..            |
             |  index_blanks ...          | column_name_n |  column_headers (level_n) |
             +----------------------------+---------------+---------------------------+
          2) |  index_names (level_0 to level_n) ...      | column_blanks ...         |
             +----------------------------+---------------+---------------------------+

        Parameters
        ----------
        blank_class : str
            CSS class added to elements within blank sections of the structure.
        blank_value : str
            HTML display value given to elements within blank sections of the structure.
        index_name_class : str
            CSS class added to elements within the index_names section of the structure.
        col_heading_class : str
            CSS class added to elements within the column_names section of structure.
        sparsify_cols : bool
            Whether column_headers section will add colspan attributes (>1) to elements.
        max_cols : int
            Maximum number of columns to render. If exceeded will contain `...` filler.
        trimmed_col_class : str
            CSS class added to elements within a column including `...` trimmed vals.

        Returns
        -------
        head : list
            The associated HTML elements needed for template rendering.
        """
        # for sparsifying a MultiIndex
        col_lengths = _get_level_lengths(
            self.columns, sparsify_cols, max_cols, self.hidden_columns
        )

        clabels = self.data.columns.tolist()[:max_cols]  # slice to allow trimming
        if self.data.columns.nlevels == 1:
            clabels = [[x] for x in clabels]
        clabels = list(zip(*clabels))

        head = []
        # 1) column headers
        if not self.hide_columns_:
            for r in range(self.data.columns.nlevels):
                index_blanks = [
                    _element("th", blank_class, blank_value, not self.hide_index_)
                ] * (self.data.index.nlevels - 1)

                name = self.data.columns.names[r]
                column_name = [
                    _element(
                        "th",
                        f"{blank_class if name is None else index_name_class} level{r}",
                        name if name is not None else blank_value,
                        not self.hide_index_,
                    )
                ]

                if clabels:
                    column_headers = [
                        _element(
                            "th",
                            f"{col_heading_class} level{r} col{c}",
                            value,
                            _is_visible(c, r, col_lengths),
                            attributes=(
                                f'colspan="{col_lengths.get((r, c), 0)}"'
                                if col_lengths.get((r, c), 0) > 1
                                else ""
                            ),
                        )
                        for c, value in enumerate(clabels[r])
                    ]

                    if len(self.data.columns) > max_cols:
                        # add an extra column with `...` value to indicate trimming
                        column_headers.append(
                            _element(
                                "th",
                                f"{col_heading_class} level{r} {trimmed_col_class}",
                                "...",
                                True,
                                attributes="",
                            )
                        )
                    head.append(index_blanks + column_name + column_headers)

        # 2) index names
        if (
            self.data.index.names
            and com.any_not_none(*self.data.index.names)
            and not self.hide_index_
            and not self.hide_columns_
        ):
            index_names = [
                _element(
                    "th",
                    f"{index_name_class} level{c}",
                    blank_value if name is None else name,
                    True,
                )
                for c, name in enumerate(self.data.index.names)
            ]

            if len(self.data.columns) <= max_cols:
                blank_len = len(clabels[0])
            else:
                blank_len = len(clabels[0]) + 1  # to allow room for `...` trim col

            column_blanks = [
                _element(
                    "th",
                    f"{blank_class} col{c}",
                    blank_value,
                    c not in self.hidden_columns,
                )
                for c in range(blank_len)
            ]
            head.append(index_names + column_blanks)

        return head
