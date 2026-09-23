    def __str__(self):
        scope_keys = _get_pretty_string(list(self.scope.keys()))
        res_keys = _get_pretty_string(list(self.resolvers.keys()))
        unicode_str = "{name}(scope={scope_keys}, resolvers={res_keys})"
        return unicode_str.format(
            name=type(self).__name__, scope_keys=scope_keys, res_keys=res_keys
        )
