    def _get_shadow(self, props: Mapping[str, str]) -> bool | None:
        if "text-shadow" in props:
            return bool(re.search("^[^#(]*[1-9]", props["text-shadow"]))
        return None
