    def __getattr__(self, attr):
        # Proxy everything that hasn't been overridden to the base
        # renderer. Things that *are* overridden can call methods
        # on self._renderer directly, but must not cache/store
        # methods (because things like RendererAgg change their
        # methods on the fly in order to optimise proxying down
        # to the underlying C implementation).
        return getattr(self._renderer, attr)
