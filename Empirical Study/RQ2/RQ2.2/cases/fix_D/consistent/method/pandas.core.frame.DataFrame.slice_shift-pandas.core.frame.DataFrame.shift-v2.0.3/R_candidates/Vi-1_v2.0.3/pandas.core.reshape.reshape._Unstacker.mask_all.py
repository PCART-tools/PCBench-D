    @cache_readonly
    def mask_all(self) -> bool:
        return bool(self.mask.all())
