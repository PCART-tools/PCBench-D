    def _delegate_property_set(self, name, value, *args, **kwargs):
        raise TypeError(f"The property {name} cannot be set")
