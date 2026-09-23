    @Appender(_shared_docs['transform'] % _shared_doc_kwargs)
    def transform(self, func, axis=0, *args, **kwargs):
        axis = self._get_axis_number(axis)
        if axis == 1:
            return super(DataFrame, self.T).transform(func, *args, **kwargs).T
        return super(DataFrame, self).transform(func, *args, **kwargs)
