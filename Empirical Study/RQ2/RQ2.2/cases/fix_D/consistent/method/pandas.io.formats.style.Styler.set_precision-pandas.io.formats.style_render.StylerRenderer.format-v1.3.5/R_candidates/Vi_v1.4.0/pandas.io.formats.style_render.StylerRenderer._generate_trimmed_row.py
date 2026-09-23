    def _generate_trimmed_row(self, max_cols: int) -> list:
        """
        When a render has too many rows we generate a trimming row containing "..."

        Parameters
        ----------
        max_cols : int
            Number of permissible columns

        Returns
        -------
        list of elements
        """
        index_headers = [
            _element(
                "th",
                (
                    f"{self.css['row_heading']} {self.css['level']}{c} "
                    f"{self.css['row_trim']}"
                ),
                "...",
                not self.hide_index_[c],
                attributes="",
            )
            for c in range(self.data.index.nlevels)
        ]

        data, visible_col_count = [], 0
        for c, _ in enumerate(self.columns):
            data_element_visible = c not in self.hidden_columns
            if data_element_visible:
                visible_col_count += 1
            if visible_col_count > max_cols:
                data.append(
                    _element(
                        "td",
                        (
                            f"{self.css['data']} {self.css['row_trim']} "
                            f"{self.css['col_trim']}"
                        ),
                        "...",
                        True,
                        attributes="",
                    )
                )
                break

            data.append(
                _element(
                    "td",
                    f"{self.css['data']} {self.css['col']}{c} {self.css['row_trim']}",
                    "...",
                    data_element_visible,
                    attributes="",
                )
            )

        return index_headers + data
