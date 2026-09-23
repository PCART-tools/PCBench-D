def _unary_method(ufunc, name):
    """Implement a unary special method with a ufunc."""
    def func(self):
        return ufunc(self)
    func.__name__ = '__{}__'.format(name)
    return func
