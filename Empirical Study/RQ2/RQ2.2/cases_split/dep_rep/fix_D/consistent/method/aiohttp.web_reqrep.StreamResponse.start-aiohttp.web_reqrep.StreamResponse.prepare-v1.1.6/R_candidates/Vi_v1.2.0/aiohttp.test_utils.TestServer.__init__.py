    def __init__(self, app, *, scheme=sentinel, host='127.0.0.1'):
        self.app = app
        self._loop = app.loop
        super().__init__(scheme=scheme, host=host)
