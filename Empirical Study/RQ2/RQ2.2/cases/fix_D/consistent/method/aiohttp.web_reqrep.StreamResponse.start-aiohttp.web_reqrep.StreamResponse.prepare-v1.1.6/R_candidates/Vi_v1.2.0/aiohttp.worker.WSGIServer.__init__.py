    def __init__(self, app, worker):
        super().__init__(app, loop=worker.loop)

        self.worker = worker
        self.access_log_format = worker._get_valid_log_format(
            worker.cfg.access_log_format)
