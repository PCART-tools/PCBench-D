    def __init__(self, name, env: PyTablesScope, side=None, encoding=None) -> None:
        assert isinstance(env, PyTablesScope), type(env)
        super().__init__(name, env, side=side, encoding=encoding)
