    def create_unbound_method(func, cls):
        return types.MethodType(func, None, cls)
