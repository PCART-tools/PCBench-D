    def _delegate_property_get(self, name):
        return getattr(self._parent, name)
