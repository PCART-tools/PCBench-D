class BasicAuth(namedtuple('BasicAuth', ['login', 'password', 'encoding'])):

    def __new__(cls, login, password='', encoding='latin1'):
        if login is None:
            raise ValueError('None is not allowed as login value')

        if password is None:
            raise ValueError('None is not allowed as login value')

        return super().__new__(cls, login, password, encoding)

    def encode(self):
        creds = ('%s:%s' % (self.login, self.password)).encode(self.encoding)
        return 'Basic %s' % base64.b64encode(creds).decode(self.encoding)
