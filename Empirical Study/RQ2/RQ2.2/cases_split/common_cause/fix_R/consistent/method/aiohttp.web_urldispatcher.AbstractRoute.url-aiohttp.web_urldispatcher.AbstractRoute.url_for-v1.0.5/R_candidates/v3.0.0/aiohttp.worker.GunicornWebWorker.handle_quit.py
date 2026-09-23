    def handle_quit(self, sig, frame):
        self.alive = False

        # worker_int callback
        self.cfg.worker_int(self)

        # wakeup closing process
        self._notify_waiter_done()
