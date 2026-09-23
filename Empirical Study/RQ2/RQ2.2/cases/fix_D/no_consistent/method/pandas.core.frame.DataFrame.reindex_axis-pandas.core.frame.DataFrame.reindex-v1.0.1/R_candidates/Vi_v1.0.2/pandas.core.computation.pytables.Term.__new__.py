    def __new__(cls, name, env, side=None, encoding=None):
        klass = Constant if not isinstance(name, str) else cls
        return object.__new__(klass)
