    @property
    def _is_boolean(self) -> bool:
        return is_bool_dtype(self.subtype)
