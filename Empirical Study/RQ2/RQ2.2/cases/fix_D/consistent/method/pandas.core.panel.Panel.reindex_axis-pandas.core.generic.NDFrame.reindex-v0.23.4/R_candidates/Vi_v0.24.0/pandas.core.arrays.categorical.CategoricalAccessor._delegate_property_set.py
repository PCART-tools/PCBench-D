    def _delegate_property_set(self, name, new_values):
        return setattr(self._parent, name, new_values)
