    def deconstruct(self):
        name, path, args, kwargs = super(OrderWrt, self).deconstruct()
        del kwargs['editable']
        return name, path, args, kwargs
