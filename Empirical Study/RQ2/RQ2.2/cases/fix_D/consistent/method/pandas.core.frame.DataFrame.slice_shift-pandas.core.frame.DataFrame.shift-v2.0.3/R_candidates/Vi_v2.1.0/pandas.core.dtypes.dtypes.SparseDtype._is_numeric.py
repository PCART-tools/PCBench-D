    @property
    def _is_numeric(self) -> bool:
        return not self.subtype == object
