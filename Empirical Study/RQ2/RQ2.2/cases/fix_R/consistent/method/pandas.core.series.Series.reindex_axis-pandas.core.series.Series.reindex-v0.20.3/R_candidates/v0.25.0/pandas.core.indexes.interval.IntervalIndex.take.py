    @Appender(_index_shared_docs["take"] % _index_doc_kwargs)
    def take(self, indices, axis=0, allow_fill=True, fill_value=None, **kwargs):
        result = self._data.take(
            indices, axis=axis, allow_fill=allow_fill, fill_value=fill_value, **kwargs
        )
        attributes = self._get_attributes_dict()
        return self._simple_new(result, **attributes)
