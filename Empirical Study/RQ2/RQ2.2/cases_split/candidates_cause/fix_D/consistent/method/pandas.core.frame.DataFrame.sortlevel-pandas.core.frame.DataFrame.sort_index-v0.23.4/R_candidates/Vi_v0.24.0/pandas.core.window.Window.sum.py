    @Substitution(name='window')
    @Appender(_shared_docs['sum'])
    def sum(self, *args, **kwargs):
        nv.validate_window_func('sum', args, kwargs)
        return self._apply_window(mean=False, **kwargs)
