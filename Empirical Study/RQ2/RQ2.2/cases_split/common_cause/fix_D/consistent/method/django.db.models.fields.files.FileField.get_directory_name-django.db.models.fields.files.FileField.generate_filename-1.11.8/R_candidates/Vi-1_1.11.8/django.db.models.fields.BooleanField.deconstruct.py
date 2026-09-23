    def deconstruct(self):
        name, path, args, kwargs = super(BooleanField, self).deconstruct()
        del kwargs['blank']
        return name, path, args, kwargs
