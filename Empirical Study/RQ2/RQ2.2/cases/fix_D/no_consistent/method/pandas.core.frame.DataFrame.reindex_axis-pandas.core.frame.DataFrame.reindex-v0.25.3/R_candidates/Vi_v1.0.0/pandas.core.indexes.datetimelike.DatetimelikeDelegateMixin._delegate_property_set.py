    def _delegate_property_set(self, name, value, *args, **kwargs):
        setattr(self._data, name, value)
