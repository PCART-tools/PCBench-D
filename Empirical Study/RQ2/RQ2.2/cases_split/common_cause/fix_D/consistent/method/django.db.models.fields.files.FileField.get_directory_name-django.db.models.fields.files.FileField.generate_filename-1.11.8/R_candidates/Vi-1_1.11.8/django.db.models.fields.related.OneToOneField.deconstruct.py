    def deconstruct(self):
        name, path, args, kwargs = super(OneToOneField, self).deconstruct()
        if "unique" in kwargs:
            del kwargs['unique']
        return name, path, args, kwargs
