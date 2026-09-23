    def _guess_content_type(self, obj, default='application/octet-stream'):
        if hasattr(obj, 'name'):
            name = getattr(obj, 'name')
            return mimetypes.guess_type(name)[0]
        elif isinstance(obj, (str, io.StringIO)):
            return 'text/plain; charset=utf-8'
        else:
            return default
