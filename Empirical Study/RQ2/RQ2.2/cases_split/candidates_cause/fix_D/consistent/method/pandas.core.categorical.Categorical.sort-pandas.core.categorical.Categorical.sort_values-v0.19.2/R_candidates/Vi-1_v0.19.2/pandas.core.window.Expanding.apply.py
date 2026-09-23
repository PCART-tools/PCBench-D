    @Substitution(name='expanding')
    @Appender(_doc_template)
    @Appender(_shared_docs['apply'])
    def apply(self, func, args=(), kwargs={}):
        return super(Expanding, self).apply(func, args=args, kwargs=kwargs)
