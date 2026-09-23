    def log_access(self, request, response, time):
        if self.access_logger is not None:
            self.access_logger.log(request, response, time)
