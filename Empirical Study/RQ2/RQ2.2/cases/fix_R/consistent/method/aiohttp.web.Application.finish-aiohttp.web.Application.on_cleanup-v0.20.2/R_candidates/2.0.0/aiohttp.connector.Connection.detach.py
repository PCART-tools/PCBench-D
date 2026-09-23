    def detach(self):
        self._notify_release()

        if self._protocol is not None:
            self._connector._release_acquired(self._protocol)
        self._protocol = None
