    def _update_font_size(
        self,
        props: dict[str, str],
        inherited: dict[str, str],
    ) -> dict[str, str]:
        # 2. resolve relative font size
        if props.get("font-size"):
            props["font-size"] = self.size_to_pt(
                props["font-size"],
                self._get_font_size(inherited),
                conversions=self.FONT_SIZE_RATIOS,
            )
        return props
