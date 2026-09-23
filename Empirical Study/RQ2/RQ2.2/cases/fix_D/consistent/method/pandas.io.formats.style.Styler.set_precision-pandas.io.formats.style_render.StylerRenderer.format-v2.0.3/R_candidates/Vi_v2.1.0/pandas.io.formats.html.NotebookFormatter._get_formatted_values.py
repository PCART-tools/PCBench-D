    def _get_formatted_values(self) -> dict[int, list[str]]:
        return {i: self.fmt.format_col(i) for i in range(self.ncols)}
