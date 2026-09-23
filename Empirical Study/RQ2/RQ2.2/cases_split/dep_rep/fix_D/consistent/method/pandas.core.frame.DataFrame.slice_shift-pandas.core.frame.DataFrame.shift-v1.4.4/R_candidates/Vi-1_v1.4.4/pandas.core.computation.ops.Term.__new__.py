    def __new__(cls, name, env, side=None, encoding=None):
        klass = Constant if not isinstance(name, str) else cls
        # error: Argument 2 for "super" not an instance of argument 1
        supr_new = super(Term, klass).__new__  # type: ignore[misc]
        return supr_new(klass)
