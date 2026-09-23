    def __init__(self, app, readpayload=False, is_ssl=False, *args, **kw):
        super().__init__(*args, **kw)

        self.wsgi = app
        self.is_ssl = is_ssl
        self.readpayload = readpayload
