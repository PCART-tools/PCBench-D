    def handle_quit(self, sig, frame):
        self.alive = False

        # worker_int callback
        self.cfg.worker_int(self)

        # init closing process
        self._closing = ensure_future(self.close(), loop=self.loop)

        # close loop
        self.loop.call_later(0.1, self._notify_waiter_done)
