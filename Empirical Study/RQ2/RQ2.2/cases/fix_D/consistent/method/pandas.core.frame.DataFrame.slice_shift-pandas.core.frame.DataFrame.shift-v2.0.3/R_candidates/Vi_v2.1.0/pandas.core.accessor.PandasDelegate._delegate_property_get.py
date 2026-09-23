    def _delegate_property_get(self, name: str, *args, **kwargs):
        raise TypeError(f"You cannot access the property {name}")
