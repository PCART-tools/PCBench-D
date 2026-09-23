    def __init__(self, value, env: PyTablesScope, side=None, encoding=None):
        assert isinstance(env, PyTablesScope), type(env)
        super().__init__(value, env, side=side, encoding=encoding)
