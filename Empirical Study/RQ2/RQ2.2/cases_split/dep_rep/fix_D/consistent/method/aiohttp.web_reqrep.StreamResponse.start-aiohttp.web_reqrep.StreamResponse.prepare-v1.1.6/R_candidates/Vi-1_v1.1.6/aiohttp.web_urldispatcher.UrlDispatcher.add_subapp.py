    def add_subapp(self, prefix, subapp):
        if subapp.frozen:
            raise RuntimeError("Cannod add frozen application")
        if prefix.endswith('/'):
            prefix = prefix[:-1]
        if prefix in ('', '/'):
            raise ValueError("Prefix cannot be empty")
        resource = PrefixedSubAppResource(prefix, subapp)
        self._reg_resource(resource)
        self._app._reg_subapp_signals(subapp)
        subapp.freeze()
        return resource
