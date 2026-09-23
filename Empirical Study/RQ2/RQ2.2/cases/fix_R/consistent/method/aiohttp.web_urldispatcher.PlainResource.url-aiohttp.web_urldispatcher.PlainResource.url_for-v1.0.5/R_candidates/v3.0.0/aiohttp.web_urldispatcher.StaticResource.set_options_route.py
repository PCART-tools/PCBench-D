    def set_options_route(self, handler):
        if 'OPTIONS' in self._routes:
            raise RuntimeError('OPTIONS route was set already')
        self._routes['OPTIONS'] = ResourceRoute(
            'OPTIONS', handler, self,
            expect_handler=self._expect_handler)
