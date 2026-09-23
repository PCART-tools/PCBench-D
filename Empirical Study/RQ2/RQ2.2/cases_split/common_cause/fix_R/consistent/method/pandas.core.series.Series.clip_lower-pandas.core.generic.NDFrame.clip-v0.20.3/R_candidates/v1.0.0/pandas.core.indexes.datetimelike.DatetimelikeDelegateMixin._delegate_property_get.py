    def _delegate_property_get(self, name, *args, **kwargs):
        result = getattr(self._data, name)
        if name not in self._raw_properties:
            result = Index(result, name=self.name)
        return result
