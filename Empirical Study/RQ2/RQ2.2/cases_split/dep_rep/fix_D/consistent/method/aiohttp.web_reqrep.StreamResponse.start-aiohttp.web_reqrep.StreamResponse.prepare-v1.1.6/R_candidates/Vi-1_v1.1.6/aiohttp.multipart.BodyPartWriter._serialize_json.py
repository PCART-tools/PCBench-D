    def _serialize_json(self, obj):
        *_, params = parse_mimetype(self.headers.get(CONTENT_TYPE))
        yield json.dumps(obj).encode(params.get('charset', 'utf-8'))
