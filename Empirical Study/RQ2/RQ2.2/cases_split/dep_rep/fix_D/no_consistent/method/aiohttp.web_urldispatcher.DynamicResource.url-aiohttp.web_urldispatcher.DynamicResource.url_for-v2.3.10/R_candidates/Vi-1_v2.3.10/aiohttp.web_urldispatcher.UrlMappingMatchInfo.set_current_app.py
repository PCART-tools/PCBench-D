    @contextmanager
    def set_current_app(self, app):
        assert app in self._apps, (
            "Expected one of the following apps {!r}, got {!r}"
            .format(self._apps, app))
        prev = self._current_app
        self._current_app = app
        try:
            yield
        finally:
            self._current_app = prev
