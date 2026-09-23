    def __iter__(self):
        return iter(self._app.router.routes())
