    @Substitution(name='expanding')
    @Appender(_shared_docs['apply'])
    def apply(self, func, raw=None, args=(), kwargs={}):
        return super(Expanding, self).apply(
            func, raw=raw, args=args, kwargs=kwargs)
