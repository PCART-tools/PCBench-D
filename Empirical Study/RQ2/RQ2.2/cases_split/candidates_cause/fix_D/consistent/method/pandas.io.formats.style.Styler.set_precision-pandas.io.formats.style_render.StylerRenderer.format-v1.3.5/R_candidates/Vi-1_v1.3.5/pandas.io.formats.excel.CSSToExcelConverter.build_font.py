    def build_font(
        self, props: Mapping[str, str]
    ) -> dict[str, bool | int | float | str | None]:
        font_names = self._get_font_names(props)
        decoration = self._get_decoration(props)
        return {
            "name": font_names[0] if font_names else None,
            "family": self._select_font_family(font_names),
            "size": self._get_font_size(props),
            "bold": self._get_is_bold(props),
            "italic": self._get_is_italic(props),
            "underline": ("single" if "underline" in decoration else None),
            "strike": ("line-through" in decoration) or None,
            "color": self.color_to_excel(props.get("color")),
            # shadow if nonzero digit before shadow color
            "shadow": self._get_shadow(props),
            # FIXME: dont leave commented-out
            # 'vertAlign':,
            # 'charset': ,
            # 'scheme': ,
            # 'outline': ,
            # 'condense': ,
        }
