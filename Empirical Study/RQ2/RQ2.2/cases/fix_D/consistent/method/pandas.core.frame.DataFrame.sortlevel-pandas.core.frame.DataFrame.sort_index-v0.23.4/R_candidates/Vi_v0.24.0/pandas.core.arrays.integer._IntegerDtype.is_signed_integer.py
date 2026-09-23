    @cache_readonly
    def is_signed_integer(self):
        return self.kind == 'i'
