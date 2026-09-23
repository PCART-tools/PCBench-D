    @property
    def header_style(self) -> dict[str, dict[str, str | bool]]:
        return {
            "font": {"bold": True},
            "borders": {
                "top": "thin",
                "right": "thin",
                "bottom": "thin",
                "left": "thin",
            },
            "alignment": {"horizontal": "center", "vertical": "top"},
        }
