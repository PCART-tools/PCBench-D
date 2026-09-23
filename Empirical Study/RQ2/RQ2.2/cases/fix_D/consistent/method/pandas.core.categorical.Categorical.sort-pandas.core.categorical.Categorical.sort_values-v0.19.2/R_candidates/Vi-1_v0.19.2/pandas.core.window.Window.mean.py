    @Substitution(name='window')
    @Appender(_doc_template)
    @Appender(_shared_docs['mean'])
    def mean(self, *args, **kwargs):
        nv.validate_window_func('mean', args, kwargs)
        return self._apply_window(mean=True, **kwargs)
