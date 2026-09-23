    def __repr__(self) -> str:
        scope_keys = _get_pretty_string(list(self.scope.keys()))
        res_keys = _get_pretty_string(list(self.resolvers.keys()))
        unicode_str = f"{type(self).__name__}(scope={scope_keys}, resolvers={res_keys})"
        return unicode_str
