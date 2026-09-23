    def _delegate_property_get(self, name, *args, **kwargs):
        raise TypeError(f"You cannot access the property {name}")
