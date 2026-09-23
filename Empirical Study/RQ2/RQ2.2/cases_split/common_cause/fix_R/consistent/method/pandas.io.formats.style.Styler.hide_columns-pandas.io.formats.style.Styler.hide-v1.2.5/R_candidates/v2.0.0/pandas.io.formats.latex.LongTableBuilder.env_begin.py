    @property
    def env_begin(self) -> str:
        first_row = (
            f"\\begin{{longtable}}{self._position_macro}{{{self.column_format}}}"
        )
        elements = [first_row, f"{self._caption_and_label()}"]
        return "\n".join([item for item in elements if item])
