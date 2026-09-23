    def _get_is_italic(self, props: Mapping[str, str]) -> bool | None:
        font_style = props.get("font-style")
        if font_style:
            return self.ITALIC_MAP.get(font_style)
        return None
