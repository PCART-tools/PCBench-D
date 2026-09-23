    @Substitution(klass='IndexOpsMixin')
    @Appender(_shared_docs['searchsorted'])
    @deprecate_kwarg(old_arg_name='key', new_arg_name='value')
    def searchsorted(self, value, side='left', sorter=None):
        # needs coercion on the key (DatetimeIndex does already)
        return self.values.searchsorted(value, side=side, sorter=sorter)
