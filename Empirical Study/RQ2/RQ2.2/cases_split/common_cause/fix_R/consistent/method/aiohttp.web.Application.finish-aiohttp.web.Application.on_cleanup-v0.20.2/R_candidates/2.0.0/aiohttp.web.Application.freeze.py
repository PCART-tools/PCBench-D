    def freeze(self):
        if self._frozen:
            return

        self._frozen = True
        self._middlewares = tuple(reversed(self._middlewares))
        self._router.freeze()
        self._on_loop_available.freeze()
        self._on_pre_signal.freeze()
        self._on_post_signal.freeze()
        self._on_response_prepare.freeze()
        self._on_startup.freeze()
        self._on_shutdown.freeze()
        self._on_cleanup.freeze()

        for subapp in self._subapps:
            subapp.freeze()
