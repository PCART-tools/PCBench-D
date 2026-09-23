    def _get_is_wrap_text(self, props: Mapping[str, str]) -> bool | None:
        if props.get("white-space") is None:
            return None
        return bool(props["white-space"] not in ("nowrap", "pre", "pre-line"))
