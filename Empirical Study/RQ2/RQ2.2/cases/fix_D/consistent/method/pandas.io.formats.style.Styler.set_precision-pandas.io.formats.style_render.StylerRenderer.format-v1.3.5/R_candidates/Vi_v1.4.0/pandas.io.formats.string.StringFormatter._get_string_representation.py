    def _get_string_representation(self) -> str:
        if self.fmt.frame.empty:
            return self._empty_info_line

        strcols = self._get_strcols()

        if self.line_width is None:
            # no need to wrap around just print the whole frame
            return self.adj.adjoin(1, *strcols)

        if self._need_to_wrap_around:
            return self._join_multiline(strcols)

        return self._fit_strcols_to_terminal_width(strcols)
