    def __init__(self, value, *args,
                 encoding=None, content_type=None, **kwargs):

        if encoding is None:
            if content_type is None:
                encoding = 'utf-8'
                content_type = 'text/plain; charset=utf-8'
            else:
                mimetype = parse_mimetype(content_type)
                encoding = mimetype.parameters.get('charset', 'utf-8')
        else:
            if content_type is None:
                content_type = 'text/plain; charset=%s' % encoding

        super().__init__(
            value.encode(encoding),
            encoding=encoding, content_type=content_type, *args, **kwargs)
