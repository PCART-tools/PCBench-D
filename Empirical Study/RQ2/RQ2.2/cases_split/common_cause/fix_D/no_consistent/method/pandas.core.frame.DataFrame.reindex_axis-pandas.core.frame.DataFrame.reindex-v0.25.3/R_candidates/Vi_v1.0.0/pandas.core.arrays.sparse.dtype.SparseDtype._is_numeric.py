    @property
    def _is_numeric(self):
        return not is_object_dtype(self.subtype)
