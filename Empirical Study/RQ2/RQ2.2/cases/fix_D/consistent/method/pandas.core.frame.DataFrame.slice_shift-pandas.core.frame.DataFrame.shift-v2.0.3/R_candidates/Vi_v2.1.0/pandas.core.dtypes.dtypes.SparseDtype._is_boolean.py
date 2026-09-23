    @property
    def _is_boolean(self) -> bool:
        return self.subtype.kind == "b"
