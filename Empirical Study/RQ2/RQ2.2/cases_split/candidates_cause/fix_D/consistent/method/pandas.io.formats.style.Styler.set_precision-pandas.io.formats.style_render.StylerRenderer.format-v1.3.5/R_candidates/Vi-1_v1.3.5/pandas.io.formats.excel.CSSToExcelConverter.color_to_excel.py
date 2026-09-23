    def color_to_excel(self, val: str | None) -> str | None:
        if val is None:
            return None

        if self._is_hex_color(val):
            return self._convert_hex_to_excel(val)

        try:
            return self.NAMED_COLORS[val]
        except KeyError:
            warnings.warn(f"Unhandled color format: {repr(val)}", CSSWarning)
        return None
