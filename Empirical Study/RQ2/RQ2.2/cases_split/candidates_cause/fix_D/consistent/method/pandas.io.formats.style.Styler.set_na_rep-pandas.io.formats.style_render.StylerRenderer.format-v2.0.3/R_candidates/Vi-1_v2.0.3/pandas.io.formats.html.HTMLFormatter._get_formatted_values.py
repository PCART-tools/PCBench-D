    def _get_formatted_values(self) -> dict[int, list[str]]:
        with option_context("display.max_colwidth", None):
            fmt_values = {i: self.fmt.format_col(i) for i in range(self.ncols)}
        return fmt_values
