    @cache_readonly
    def is_unsigned_integer(self):
        return self.kind == 'u'
