    def add_subapp(self, prefix, subapp):
        if self.frozen:
            raise RuntimeError(
                "Cannot add sub application to frozen application")
        if subapp.frozen:
            raise RuntimeError("Cannot add frozen application")
        if prefix.endswith('/'):
            prefix = prefix[:-1]
        if prefix in ('', '/'):
            raise ValueError("Prefix cannot be empty")

        resource = PrefixedSubAppResource(prefix, subapp)
        self.router.register_resource(resource)
        self._reg_subapp_signals(subapp)
        self._subapps.append(subapp)
        subapp.freeze()
        if self._loop is not None:
            subapp._set_loop(self._loop)
        return resource
