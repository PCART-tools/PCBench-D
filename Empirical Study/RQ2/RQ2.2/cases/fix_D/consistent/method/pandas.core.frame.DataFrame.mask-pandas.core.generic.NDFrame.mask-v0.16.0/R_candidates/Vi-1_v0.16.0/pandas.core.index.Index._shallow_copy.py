    def _shallow_copy(self, values=None, **kwargs):
        """ create a new Index, don't copy the data, use the same object attributes
            with passed in attributes taking precedence """
        if values is None:
            values = self.values
        attributes = self._get_attributes_dict()
        attributes.update(kwargs)
        return self.__class__._simple_new(values,**attributes)
