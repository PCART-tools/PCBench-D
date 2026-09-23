    def _translate_latex(self, d: dict, clines: str | None) -> None:
        r"""
        Post-process the default render dict for the LaTeX template format.

        Processing items included are:
          - Remove hidden columns from the non-headers part of the body.
          - Place cellstyles directly in td cells rather than use cellstyle_map.
          - Remove hidden indexes or reinsert missing th elements if part of multiindex
            or multirow sparsification (so that \multirow and \multicol work correctly).
        """
        index_levels = self.index.nlevels
        visible_index_level_n = index_levels - sum(self.hide_index_)
        d["head"] = [
            [
                {**col, "cellstyle": self.ctx_columns[r, c - visible_index_level_n]}
                for c, col in enumerate(row)
                if col["is_visible"]
            ]
            for r, row in enumerate(d["head"])
        ]

        def _concatenated_visible_rows(obj, n, row_indices):
            """
            Extract all visible row indices recursively from concatenated stylers.
            """
            row_indices.extend(
                [r + n for r in range(len(obj.index)) if r not in obj.hidden_rows]
            )
            n += len(obj.index)
            for concatenated in obj.concatenated:
                n = _concatenated_visible_rows(concatenated, n, row_indices)
            return n

        def concatenated_visible_rows(obj):
            row_indices: list[int] = []
            _concatenated_visible_rows(obj, 0, row_indices)
            # TODO try to consolidate the concat visible rows
            # methods to a single function / recursion for simplicity
            return row_indices

        body = []
        for r, row in zip(concatenated_visible_rows(self), d["body"]):
            # note: cannot enumerate d["body"] because rows were dropped if hidden
            # during _translate_body so must zip to acquire the true r-index associated
            # with the ctx obj which contains the cell styles.
            if all(self.hide_index_):
                row_body_headers = []
            else:
                row_body_headers = [
                    {
                        **col,
                        "display_value": col["display_value"]
                        if col["is_visible"]
                        else "",
                        "cellstyle": self.ctx_index[r, c],
                    }
                    for c, col in enumerate(row[:index_levels])
                    if (col["type"] == "th" and not self.hide_index_[c])
                ]

            row_body_cells = [
                {**col, "cellstyle": self.ctx[r, c]}
                for c, col in enumerate(row[index_levels:])
                if (col["is_visible"] and col["type"] == "td")
            ]

            body.append(row_body_headers + row_body_cells)
        d["body"] = body

        # clines are determined from info on index_lengths and hidden_rows and input
        # to a dict defining which row clines should be added in the template.
        if clines not in [
            None,
            "all;data",
            "all;index",
            "skip-last;data",
            "skip-last;index",
        ]:
            raise ValueError(
                f"`clines` value of {clines} is invalid. Should either be None or one "
                f"of 'all;data', 'all;index', 'skip-last;data', 'skip-last;index'."
            )
        if clines is not None:
            data_len = len(row_body_cells) if "data" in clines and d["body"] else 0

            d["clines"] = defaultdict(list)
            visible_row_indexes: list[int] = [
                r for r in range(len(self.data.index)) if r not in self.hidden_rows
            ]
            visible_index_levels: list[int] = [
                i for i in range(index_levels) if not self.hide_index_[i]
            ]
            for rn, r in enumerate(visible_row_indexes):
                for lvln, lvl in enumerate(visible_index_levels):
                    if lvl == index_levels - 1 and "skip-last" in clines:
                        continue
                    idx_len = d["index_lengths"].get((lvl, r), None)
                    if idx_len is not None:  # i.e. not a sparsified entry
                        d["clines"][rn + idx_len].append(
                            f"\\cline{{{lvln+1}-{len(visible_index_levels)+data_len}}}"
                        )
