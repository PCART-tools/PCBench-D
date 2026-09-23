    def __new__(cls, name, env, side=None, encoding=None):
        if isinstance(name, str):
            klass = cls
        else:
            klass = Constant
        return object.__new__(klass)
