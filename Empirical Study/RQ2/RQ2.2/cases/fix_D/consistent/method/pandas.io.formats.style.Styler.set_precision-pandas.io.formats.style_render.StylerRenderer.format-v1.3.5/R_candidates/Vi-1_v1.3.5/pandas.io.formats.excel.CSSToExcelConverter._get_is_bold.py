    def _get_is_bold(self, props: Mapping[str, str]) -> bool | None:
        weight = props.get("font-weight")
        if weight:
            return self.BOLD_MAP.get(weight)
        return None
