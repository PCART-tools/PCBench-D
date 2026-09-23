    def __init__(self, prefix, app):
        super().__init__(prefix)
        self._app = app
        for resource in app.router.resources():
            resource.add_prefix(prefix)
