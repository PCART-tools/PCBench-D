    @Appender(_index_shared_docs["_shallow_copy"])
    def _shallow_copy(self, left=None, right=None, **kwargs):
        result = self._data._shallow_copy(left=left, right=right)
        attributes = self._get_attributes_dict()
        attributes.update(kwargs)
        return self._simple_new(result, **attributes)
