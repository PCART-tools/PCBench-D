    def deconstruct(self):
        name, path, args, kwargs = super(IPAddressField, self).deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs
