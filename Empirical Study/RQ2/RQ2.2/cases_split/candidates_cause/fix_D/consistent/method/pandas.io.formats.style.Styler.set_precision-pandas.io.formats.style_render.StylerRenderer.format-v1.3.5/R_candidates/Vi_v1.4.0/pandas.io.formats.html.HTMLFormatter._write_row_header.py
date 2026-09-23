    def _write_row_header(self, indent: int) -> None:
        is_truncated_horizontally = self.fmt.is_truncated_horizontally
        row = [x if x is not None else "" for x in self.frame.index.names] + [""] * (
            self.ncols + (1 if is_truncated_horizontally else 0)
        )
        self.write_tr(row, indent, self.indent_delta, header=True)
