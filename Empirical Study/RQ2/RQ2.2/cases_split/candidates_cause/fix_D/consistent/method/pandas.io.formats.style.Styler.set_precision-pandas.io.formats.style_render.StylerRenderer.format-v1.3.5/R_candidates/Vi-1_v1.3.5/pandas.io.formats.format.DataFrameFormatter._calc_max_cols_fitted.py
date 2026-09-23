    def _calc_max_cols_fitted(self) -> int | None:
        """Number of columns fitting the screen."""
        if not self._is_in_terminal():
            return self.max_cols

        width, _ = get_terminal_size()
        if self._is_screen_narrow(width):
            return width
        else:
            return self.max_cols
