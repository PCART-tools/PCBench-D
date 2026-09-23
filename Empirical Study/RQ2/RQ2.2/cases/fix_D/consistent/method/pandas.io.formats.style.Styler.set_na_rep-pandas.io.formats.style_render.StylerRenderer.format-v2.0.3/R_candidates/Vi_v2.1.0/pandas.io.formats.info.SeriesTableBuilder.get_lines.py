    def get_lines(self) -> list[str]:
        self._lines = []
        self._fill_non_empty_info()
        return self._lines
