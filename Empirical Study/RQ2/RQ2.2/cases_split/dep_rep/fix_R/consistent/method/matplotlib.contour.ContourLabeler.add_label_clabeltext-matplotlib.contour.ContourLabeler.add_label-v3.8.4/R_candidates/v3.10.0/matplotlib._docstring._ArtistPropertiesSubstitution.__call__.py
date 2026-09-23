    def __call__(self, obj):
        if obj.__doc__:
            obj.__doc__ = inspect.cleandoc(obj.__doc__) % self.params
        if isinstance(obj, type) and obj.__init__ != object.__init__:
            self(obj.__init__)
        return obj
