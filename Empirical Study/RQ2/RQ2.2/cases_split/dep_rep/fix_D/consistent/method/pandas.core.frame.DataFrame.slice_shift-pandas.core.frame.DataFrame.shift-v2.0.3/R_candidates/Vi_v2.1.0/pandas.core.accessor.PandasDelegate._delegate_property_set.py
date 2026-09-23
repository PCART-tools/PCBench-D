    def _delegate_property_set(self, name: str, value, *args, **kwargs):
        raise TypeError(f"The property {name} cannot be set")
