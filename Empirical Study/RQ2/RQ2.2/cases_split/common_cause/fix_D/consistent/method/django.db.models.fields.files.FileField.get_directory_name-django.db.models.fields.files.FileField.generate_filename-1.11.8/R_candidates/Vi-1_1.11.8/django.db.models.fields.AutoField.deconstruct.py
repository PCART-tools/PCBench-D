    def deconstruct(self):
        name, path, args, kwargs = super(AutoField, self).deconstruct()
        del kwargs['blank']
        kwargs['primary_key'] = True
        return name, path, args, kwargs
