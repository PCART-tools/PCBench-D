    @asyncio.coroutine
    def post(self):
        """Return POST parameters."""
        if self._post is not None:
            return self._post
        if self.method not in self.POST_METHODS:
            self._post = MultiDictProxy(MultiDict())
            return self._post

        content_type = self.content_type
        if (content_type not in ('',
                                 'application/x-www-form-urlencoded',
                                 'multipart/form-data')):
            self._post = MultiDictProxy(MultiDict())
            return self._post

        if self.content_type.startswith('multipart/'):
            warnings.warn('To process multipart requests use .multipart'
                          ' coroutine instead.', DeprecationWarning)

        body = yield from self.read()
        content_charset = self.charset or 'utf-8'

        environ = {'REQUEST_METHOD': self.method,
                   'CONTENT_LENGTH': str(len(body)),
                   'QUERY_STRING': '',
                   'CONTENT_TYPE': self.headers.get(hdrs.CONTENT_TYPE)}

        fs = cgi.FieldStorage(fp=io.BytesIO(body),
                              environ=environ,
                              keep_blank_values=True,
                              encoding=content_charset)

        supported_transfer_encoding = {
            'base64': binascii.a2b_base64,
            'quoted-printable': binascii.a2b_qp
        }

        out = MultiDict()
        _count = 1
        for field in fs.list or ():
            transfer_encoding = field.headers.get(
                hdrs.CONTENT_TRANSFER_ENCODING, None)
            if field.filename:
                ff = FileField(field.name,
                               field.filename,
                               field.file,  # N.B. file closed error
                               field.type)
                if self._post_files_cache is None:
                    self._post_files_cache = {}
                self._post_files_cache[field.name+str(_count)] = field
                _count += 1
                out.add(field.name, ff)
            else:
                value = field.value
                if transfer_encoding in supported_transfer_encoding:
                    # binascii accepts bytes
                    value = value.encode('utf-8')
                    value = supported_transfer_encoding[
                        transfer_encoding](value)
                out.add(field.name, value)

        self._post = MultiDictProxy(out)
        return self._post
