    def get_charset(self, default=None):
        """Returns charset parameter from Content-Type header or default."""
        ctype = self.headers.get(CONTENT_TYPE, '')
        mimetype = parse_mimetype(ctype)
        return mimetype.parameters.get('charset', default)
