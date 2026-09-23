    @property
    def request_info(self):
        return RequestInfo(self.url, self.method, self.headers)
