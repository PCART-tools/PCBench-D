    def deconstruct(self):
        name, path, args, kwargs = super(URLField, self).deconstruct()
        if kwargs.get("max_length") == 200:
            del kwargs['max_length']
        return name, path, args, kwargs
