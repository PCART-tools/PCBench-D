    def log_debug(self, *args, **kw):
        if self.debug:
            self.logger.debug(*args, **kw)
