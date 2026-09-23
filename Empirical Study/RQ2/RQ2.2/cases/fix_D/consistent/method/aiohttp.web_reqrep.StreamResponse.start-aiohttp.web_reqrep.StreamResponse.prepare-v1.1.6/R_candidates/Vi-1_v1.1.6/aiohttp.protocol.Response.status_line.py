    @reify
    def status_line(self):
        version = self.version
        return 'HTTP/{}.{} {} {}\r\n'.format(
            version[0], version[1], self.status, self.reason)
