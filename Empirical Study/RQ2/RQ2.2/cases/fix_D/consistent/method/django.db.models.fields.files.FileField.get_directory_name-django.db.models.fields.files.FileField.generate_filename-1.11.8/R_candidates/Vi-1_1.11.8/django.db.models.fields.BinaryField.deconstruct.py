    def deconstruct(self):
        name, path, args, kwargs = super(BinaryField, self).deconstruct()
        del kwargs['editable']
        return name, path, args, kwargs
