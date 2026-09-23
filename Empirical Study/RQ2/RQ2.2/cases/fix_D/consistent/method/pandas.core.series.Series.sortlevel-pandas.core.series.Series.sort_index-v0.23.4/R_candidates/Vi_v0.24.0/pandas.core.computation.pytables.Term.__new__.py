    def __new__(cls, name, env, side=None, encoding=None):
        klass = Constant if not isinstance(name, string_types) else cls
        supr_new = StringMixin.__new__
        return supr_new(klass)
