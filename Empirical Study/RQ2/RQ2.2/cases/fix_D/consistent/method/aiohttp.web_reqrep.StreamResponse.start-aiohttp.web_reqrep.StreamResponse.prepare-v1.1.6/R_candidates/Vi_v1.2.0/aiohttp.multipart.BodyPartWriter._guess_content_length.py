    def _guess_content_length(self, obj):
        if isinstance(obj, bytes):
            return len(obj)
        elif isinstance(obj, str):
            *_, params = parse_mimetype(self.headers.get(CONTENT_TYPE))
            charset = params.get('charset', 'us-ascii')
            return len(obj.encode(charset))
        elif isinstance(obj, io.StringIO):
            *_, params = parse_mimetype(self.headers.get(CONTENT_TYPE))
            charset = params.get('charset', 'us-ascii')
            return len(obj.getvalue().encode(charset)) - obj.tell()
        elif isinstance(obj, io.BytesIO):
            return len(obj.getvalue()) - obj.tell()
        elif isinstance(obj, io.IOBase):
            try:
                return os.fstat(obj.fileno()).st_size - obj.tell()
            except (AttributeError, OSError):
                return None
        else:
            return None
