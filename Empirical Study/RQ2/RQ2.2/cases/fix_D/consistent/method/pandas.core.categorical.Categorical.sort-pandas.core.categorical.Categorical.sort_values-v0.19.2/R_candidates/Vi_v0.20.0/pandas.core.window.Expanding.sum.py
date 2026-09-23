    @Substitution(name='expanding')
    @Appender(_doc_template)
    @Appender(_shared_docs['sum'])
    def sum(self, *args, **kwargs):
        nv.validate_expanding_func('sum', args, kwargs)
        return super(Expanding, self).sum(*args, **kwargs)
