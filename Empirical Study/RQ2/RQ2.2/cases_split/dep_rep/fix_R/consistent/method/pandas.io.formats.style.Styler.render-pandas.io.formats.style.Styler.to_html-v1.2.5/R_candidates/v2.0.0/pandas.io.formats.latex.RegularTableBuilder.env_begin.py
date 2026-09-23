    @property
    def env_begin(self) -> str:
        elements = [
            f"\\begin{{table}}{self._position_macro}",
            "\\centering",
            f"{self._caption_macro}",
            f"{self._label_macro}",
            f"\\begin{{tabular}}{{{self.column_format}}}",
        ]
        return "\n".join([item for item in elements if item])
