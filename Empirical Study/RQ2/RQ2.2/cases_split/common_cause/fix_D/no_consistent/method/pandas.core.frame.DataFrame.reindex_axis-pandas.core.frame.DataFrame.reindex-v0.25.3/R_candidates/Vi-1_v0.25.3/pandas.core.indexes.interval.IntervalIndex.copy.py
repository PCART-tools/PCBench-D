    @Appender(_index_shared_docs["copy"])
    def copy(self, deep=False, name=None):
        array = self._data
        if deep:
            array = array.copy()
        attributes = self._get_attributes_dict()
        if name is not None:
            attributes.update(name=name)

        return self._simple_new(array, **attributes)
