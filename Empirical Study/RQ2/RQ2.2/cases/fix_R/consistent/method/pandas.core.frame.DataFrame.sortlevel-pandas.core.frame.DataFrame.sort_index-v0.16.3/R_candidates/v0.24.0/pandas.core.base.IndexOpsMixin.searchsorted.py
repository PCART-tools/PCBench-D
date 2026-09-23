    @Substitution(klass='IndexOpsMixin')
    @Appender(_shared_docs['searchsorted'])
    def searchsorted(self, value, side='left', sorter=None):
        # needs coercion on the key (DatetimeIndex does already)
        return self._values.searchsorted(value, side=side, sorter=sorter)
