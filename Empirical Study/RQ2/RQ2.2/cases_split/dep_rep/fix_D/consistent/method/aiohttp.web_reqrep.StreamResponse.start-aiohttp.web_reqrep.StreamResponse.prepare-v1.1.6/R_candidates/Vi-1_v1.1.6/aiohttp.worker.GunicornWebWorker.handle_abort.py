    def handle_abort(self, sig, frame):
        self.alive = False
        self.exit_code = 1
