    def get_charset(self, default=None):
        """Returns charset parameter from ``Content-Type`` header or default.
        """
        ctype = self.headers.get(CONTENT_TYPE, '')
        *_, params = parse_mimetype(ctype)
        return params.get('charset', default)
