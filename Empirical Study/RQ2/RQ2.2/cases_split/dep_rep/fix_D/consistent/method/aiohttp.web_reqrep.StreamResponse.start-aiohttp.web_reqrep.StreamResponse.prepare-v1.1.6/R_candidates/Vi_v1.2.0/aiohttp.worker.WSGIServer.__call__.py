    def __call__(self):
        return WSGIServerHttpProtocol(
            self.handler, readpayload=True,
            loop=self._loop,
            logger=self.worker.log,
            debug=self.worker.log.loglevel == logging.DEBUG,
            keep_alive=self.worker.cfg.keepalive,
            access_log=self.worker.log.access_log,
            access_log_format=self.access_log_format)
