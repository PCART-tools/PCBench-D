    def run(self):
        access_log = self.log.access_log if self.cfg.accesslog else None
        params = dict(
            logger=self.log,
            keepalive_timeout=self.cfg.keepalive,
            access_log=access_log,
            access_log_format=self._get_valid_log_format(
                self.cfg.access_log_format))
        self._runner = web.AppRunner(self.wsgi, **params)
        self.loop.run_until_complete(self._runner.setup())
        self._task = self.loop.create_task(self._run())

        with suppress(Exception):  # ignore all finalization problems
            self.loop.run_until_complete(self._task)
        if hasattr(self.loop, 'shutdown_asyncgens'):
            self.loop.run_until_complete(self.loop.shutdown_asyncgens())
        self.loop.close()

        sys.exit(self.exit_code)
