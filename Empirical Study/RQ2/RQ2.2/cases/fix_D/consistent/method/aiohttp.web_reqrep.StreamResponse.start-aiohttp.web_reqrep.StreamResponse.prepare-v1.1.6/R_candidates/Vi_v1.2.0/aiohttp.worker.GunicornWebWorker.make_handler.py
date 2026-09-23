    def make_handler(self, app):
        if hasattr(self.wsgi, 'make_handler'):
            return app.make_handler(
                logger=self.log,
                slow_request_timeout=self.cfg.timeout,
                keepalive_timeout=self.cfg.keepalive,
                access_log=self.log.access_log,
                access_log_format=self._get_valid_log_format(
                    self.cfg.access_log_format))
        else:
            return WSGIServer(self.wsgi, self)
