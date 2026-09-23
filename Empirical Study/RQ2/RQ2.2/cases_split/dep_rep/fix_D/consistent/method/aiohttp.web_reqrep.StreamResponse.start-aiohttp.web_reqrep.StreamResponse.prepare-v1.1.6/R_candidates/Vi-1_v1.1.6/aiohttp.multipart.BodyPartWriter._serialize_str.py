    def _serialize_str(self, obj):
        *_, params = parse_mimetype(self.headers.get(CONTENT_TYPE))
        yield obj.encode(params.get('charset', 'us-ascii'))
