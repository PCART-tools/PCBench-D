    def __len__(self):
        return len(self._app.router.routes())
