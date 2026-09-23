    def _get_font_size(self, props: Mapping[str, str]) -> float | None:
        size = props.get("font-size")
        if size is None:
            return size
        return self._pt_to_float(size)
