    def __init__(self, app, *,
                 scheme=sentinel, host='127.0.0.1', **kwargs):
        self.app = app
        super().__init__(scheme=scheme, host=host, **kwargs)
