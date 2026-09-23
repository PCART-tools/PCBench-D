    def instancemethod(func, obj, cls):
        return types.MethodType(func, obj)
