    @reify
    def status_line(self):
        return '{0} {1} HTTP/{2[0]}.{2[1]}\r\n'.format(
            self.method, self.path, self.version)
