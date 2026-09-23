    @property
    def boundary(self):
        *_, params = parse_mimetype(self.headers.get(CONTENT_TYPE))
        return params['boundary'].encode('us-ascii')
