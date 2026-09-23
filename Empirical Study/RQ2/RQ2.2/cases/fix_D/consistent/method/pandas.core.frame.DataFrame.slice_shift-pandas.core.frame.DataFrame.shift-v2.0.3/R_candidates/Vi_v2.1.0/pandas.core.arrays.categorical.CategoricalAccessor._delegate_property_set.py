    def _delegate_property_set(self, name: str, new_values):  # type: ignore[override]
        return setattr(self._parent, name, new_values)
