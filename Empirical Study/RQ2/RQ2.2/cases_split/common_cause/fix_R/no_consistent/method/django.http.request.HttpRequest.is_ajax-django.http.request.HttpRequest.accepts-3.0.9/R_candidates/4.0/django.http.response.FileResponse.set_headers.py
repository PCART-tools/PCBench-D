    def set_headers(self, filelike):
        """
        Set some common response headers (Content-Length, Content-Type, and
        Content-Disposition) based on the `filelike` response content.
        """
        encoding_map = {
            'bzip2': 'application/x-bzip',
            'gzip': 'application/gzip',
            'xz': 'application/x-xz',
        }
        filename = getattr(filelike, 'name', None)
        filename = filename if (isinstance(filename, str) and filename) else self.filename
        if os.path.isabs(filename):
            self.headers['Content-Length'] = os.path.getsize(filelike.name)
        elif hasattr(filelike, 'getbuffer'):
            self.headers['Content-Length'] = filelike.getbuffer().nbytes

        if self.headers.get('Content-Type', '').startswith('text/html'):
            if filename:
                content_type, encoding = mimetypes.guess_type(filename)
                # Encoding isn't set to prevent browsers from automatically
                # uncompressing files.
                content_type = encoding_map.get(encoding, content_type)
                self.headers['Content-Type'] = content_type or 'application/octet-stream'
            else:
                self.headers['Content-Type'] = 'application/octet-stream'

        filename = self.filename or os.path.basename(filename)
        if filename:
            disposition = 'attachment' if self.as_attachment else 'inline'
            try:
                filename.encode('ascii')
                file_expr = 'filename="{}"'.format(filename)
            except UnicodeEncodeError:
                file_expr = "filename*=utf-8''{}".format(quote(filename))
            self.headers['Content-Disposition'] = '{}; {}'.format(disposition, file_expr)
        elif self.as_attachment:
            self.headers['Content-Disposition'] = 'attachment'
