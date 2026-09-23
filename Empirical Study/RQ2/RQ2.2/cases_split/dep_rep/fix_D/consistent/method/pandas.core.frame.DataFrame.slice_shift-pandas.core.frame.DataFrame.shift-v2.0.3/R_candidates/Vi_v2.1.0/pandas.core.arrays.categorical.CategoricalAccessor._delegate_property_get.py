    def _delegate_property_get(self, name: str):  # type: ignore[override]
        return getattr(self._parent, name)
