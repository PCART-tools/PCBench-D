    def _delegate_property_get(self, name, *args, **kwargs):
        return getattr(self._parent.array, name)
