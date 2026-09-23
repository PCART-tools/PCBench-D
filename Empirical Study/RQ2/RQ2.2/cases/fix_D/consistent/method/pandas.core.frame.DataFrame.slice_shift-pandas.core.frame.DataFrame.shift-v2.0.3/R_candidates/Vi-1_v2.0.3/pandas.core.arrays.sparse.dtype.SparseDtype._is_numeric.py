    @property
    def _is_numeric(self) -> bool:
        return not is_object_dtype(self.subtype)
