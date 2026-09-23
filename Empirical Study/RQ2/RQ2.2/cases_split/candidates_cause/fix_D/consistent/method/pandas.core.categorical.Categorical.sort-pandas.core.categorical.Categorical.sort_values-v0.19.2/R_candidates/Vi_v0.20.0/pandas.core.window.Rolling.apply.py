    @Substitution(name='rolling')
    @Appender(_doc_template)
    @Appender(_shared_docs['apply'])
    def apply(self, func, args=(), kwargs={}):
        return super(Rolling, self).apply(func, args=args, kwargs=kwargs)
