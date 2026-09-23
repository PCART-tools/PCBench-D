    def __init__(self, app):
        super().__init__()
        self._app = app
        klass = self.__class__
        self._name = klass.__module__ + ':' + klass.__qualname__
        self._pre = app.on_pre_signal
        self._post = app.on_post_signal
