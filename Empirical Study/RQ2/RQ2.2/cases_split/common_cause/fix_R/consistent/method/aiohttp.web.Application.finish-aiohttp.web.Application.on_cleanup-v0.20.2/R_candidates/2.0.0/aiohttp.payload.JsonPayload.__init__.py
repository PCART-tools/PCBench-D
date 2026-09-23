    def __init__(self, value,
                 encoding='utf-8', content_type='application/json',
                 dumps=json.dumps, *args, **kwargs):

        super().__init__(
            dumps(value).encode(encoding),
            content_type=content_type, encoding=encoding, *args, **kwargs)
