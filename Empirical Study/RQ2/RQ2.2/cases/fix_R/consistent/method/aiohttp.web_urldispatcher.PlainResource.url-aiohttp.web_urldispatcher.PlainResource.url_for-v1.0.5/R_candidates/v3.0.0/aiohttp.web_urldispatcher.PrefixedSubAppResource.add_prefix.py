    def add_prefix(self, prefix):
        super().add_prefix(prefix)
        for resource in self._app.router.resources():
            resource.add_prefix(prefix)
