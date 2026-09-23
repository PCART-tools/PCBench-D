    def __str__(self):
        return ('Cannot connect to host {0.host}:{0.port} ssl:{0.ssl} '
                '[{0.certificate_error.__class__.__name__}: '
                '{0.certificate_error.args}]'.format(self))
