    def _get_encoding(self):
        ctype = self.headers.get(hdrs.CONTENT_TYPE, '').lower()
        mtype, stype, _, params = helpers.parse_mimetype(ctype)

        encoding = params.get('charset')
        if not encoding:
            if mtype == 'application' and stype == 'json':
                # RFC 7159 states that the default encoding is UTF-8.
                encoding = 'utf-8'
            else:
                encoding = chardet.detect(self._content)['encoding']
        if not encoding:
            encoding = 'utf-8'

        return encoding
