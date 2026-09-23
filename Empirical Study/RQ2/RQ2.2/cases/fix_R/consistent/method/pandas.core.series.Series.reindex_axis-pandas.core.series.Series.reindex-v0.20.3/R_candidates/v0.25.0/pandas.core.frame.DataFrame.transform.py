    @Appender(_shared_docs["transform"] % _shared_doc_kwargs)
    def transform(self, func, axis=0, *args, **kwargs):
        axis = self._get_axis_number(axis)
        if axis == 1:
            return self.T.transform(func, *args, **kwargs).T
        return super().transform(func, *args, **kwargs)
