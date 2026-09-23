    def deconstruct(self):
        name, path, args, kwargs = super(NullBooleanField, self).deconstruct()
        del kwargs['null']
        del kwargs['blank']
        return name, path, args, kwargs
