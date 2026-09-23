    def _write_body(self, indent: int) -> None:
        self.write("<tbody>", indent)
        fmt_values = self._get_formatted_values()

        # write values
        if self.fmt.index and isinstance(self.frame.index, MultiIndex):
            self._write_hierarchical_rows(fmt_values, indent + self.indent_delta)
        else:
            self._write_regular_rows(fmt_values, indent + self.indent_delta)

        self.write("</tbody>", indent)
