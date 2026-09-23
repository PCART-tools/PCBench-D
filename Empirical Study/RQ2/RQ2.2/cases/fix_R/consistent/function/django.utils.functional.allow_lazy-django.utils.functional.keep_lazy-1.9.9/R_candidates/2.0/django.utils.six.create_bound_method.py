    def create_bound_method(func, obj):
        return types.MethodType(func, obj, obj.__class__)
