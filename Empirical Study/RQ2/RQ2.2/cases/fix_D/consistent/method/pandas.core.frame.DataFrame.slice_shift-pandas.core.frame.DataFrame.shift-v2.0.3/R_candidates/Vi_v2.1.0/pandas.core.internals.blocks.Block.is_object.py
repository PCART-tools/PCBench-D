    @final
    @cache_readonly
    def is_object(self) -> bool:
        return self.values.dtype == _dtype_obj
