    def _delegate_property_get(self, name, *args, **kwargs):
        raise TypeError("You cannot access the " "property {name}".format(name=name))
