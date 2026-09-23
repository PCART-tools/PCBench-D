    @Substitution(klass='IndexOpsMixin', value='key')
    @Appender(_shared_docs['searchsorted'])
    def searchsorted(self, key, side='left', sorter=None):
        # needs coercion on the key (DatetimeIndex does already)
        return self.values.searchsorted(key, side=side, sorter=sorter)
