    def _get_strcols_without_index(self) -> list[list[str]]:
        strcols: list[list[str]] = []

        if not is_list_like(self.header) and not self.header:
            for i, c in enumerate(self.tr_frame):
                fmt_values = self.format_col(i)
                fmt_values = _make_fixed_width(
                    strings=fmt_values,
                    justify=self.justify,
                    minimum=int(self.col_space.get(c, 0)),
                    adj=self.adj,
                )
                strcols.append(fmt_values)
            return strcols

        if is_list_like(self.header):
            # cast here since can't be bool if is_list_like
            self.header = cast(list[str], self.header)
            if len(self.header) != len(self.columns):
                raise ValueError(
                    f"Writing {len(self.columns)} cols "
                    f"but got {len(self.header)} aliases"
                )
            str_columns = [[label] for label in self.header]
        else:
            str_columns = self._get_formatted_column_labels(self.tr_frame)

        if self.show_row_idx_names:
            for x in str_columns:
                x.append("")

        for i, c in enumerate(self.tr_frame):
            cheader = str_columns[i]
            header_colwidth = max(
                int(self.col_space.get(c, 0)), *(self.adj.len(x) for x in cheader)
            )
            fmt_values = self.format_col(i)
            fmt_values = _make_fixed_width(
                fmt_values, self.justify, minimum=header_colwidth, adj=self.adj
            )

            max_len = max(*(self.adj.len(x) for x in fmt_values), header_colwidth)
            cheader = self.adj.justify(cheader, max_len, mode=self.justify)
            strcols.append(cheader + fmt_values)

        return strcols
