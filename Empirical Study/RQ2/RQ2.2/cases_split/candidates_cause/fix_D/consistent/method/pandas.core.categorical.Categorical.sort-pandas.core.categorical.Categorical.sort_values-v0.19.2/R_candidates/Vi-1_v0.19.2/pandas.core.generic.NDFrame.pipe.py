    @Appender(_shared_docs['pipe'] % _shared_doc_kwargs)
    def pipe(self, func, *args, **kwargs):
        if isinstance(func, tuple):
            func, target = func
            if target in kwargs:
                raise ValueError('%s is both the pipe target and a keyword '
                                 'argument' % target)
            kwargs[target] = self
            return func(*args, **kwargs)
        else:
            return func(self, *args, **kwargs)
