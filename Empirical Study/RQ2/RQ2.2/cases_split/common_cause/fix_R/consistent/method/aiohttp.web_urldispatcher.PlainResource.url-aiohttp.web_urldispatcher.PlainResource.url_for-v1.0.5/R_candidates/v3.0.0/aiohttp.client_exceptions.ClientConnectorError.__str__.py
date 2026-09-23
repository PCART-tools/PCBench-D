    def __str__(self):
        return ('Cannot connect to host {0.host}:{0.port} ssl:{0.ssl} [{1}]'
                .format(self, self.strerror))
