    def _get_float_font_size_from_pt(self, font_size_string: str) -> float:
        assert font_size_string.endswith("pt")
        return float(font_size_string.rstrip("pt"))
