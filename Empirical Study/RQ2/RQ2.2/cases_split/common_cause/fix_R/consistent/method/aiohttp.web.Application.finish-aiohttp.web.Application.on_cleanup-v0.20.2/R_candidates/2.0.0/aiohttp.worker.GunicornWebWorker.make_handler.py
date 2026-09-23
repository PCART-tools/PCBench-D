    def make_handler(self, app):
        if hasattr(self.wsgi, 'make_handler'):
            access_log = self.log.access_log if self.cfg.accesslog else None
            return app.make_handler(
                loop=self.loop,
                logger=self.log,
                slow_request_timeout=self.cfg.timeout,
                keepalive_timeout=self.cfg.keepalive,
                access_log=access_log,
                access_log_format=self._get_valid_log_format(
                    self.cfg.access_log_format))
        else:
            raise RuntimeError(
                "aiohttp.wsgi is not supported anymore, "
                "consider to switch to aiohttp.web.Application")
