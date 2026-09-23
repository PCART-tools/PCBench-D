    async def post(self):
        """Return POST parameters."""
        if self._post is not None:
            return self._post
        if self._method not in self.POST_METHODS:
            self._post = MultiDictProxy(MultiDict())
            return self._post

        content_type = self.content_type
        if (content_type not in ('',
                                 'application/x-www-form-urlencoded',
                                 'multipart/form-data')):
            self._post = MultiDictProxy(MultiDict())
            return self._post

        out = MultiDict()

        if content_type == 'multipart/form-data':
            multipart = await self.multipart()

            field = await multipart.next()
            while field is not None:
                size = 0
                max_size = self._client_max_size
                content_type = field.headers.get(hdrs.CONTENT_TYPE)

                if field.filename:
                    # store file in temp file
                    tmp = tempfile.TemporaryFile()
                    chunk = await field.read_chunk(size=2**16)
                    while chunk:
                        chunk = field.decode(chunk)
                        tmp.write(chunk)
                        size += len(chunk)
                        if 0 < max_size < size:
                            raise ValueError(
                                'Maximum request body size exceeded')
                        chunk = await field.read_chunk(size=2**16)
                    tmp.seek(0)

                    ff = FileField(field.name, field.filename,
                                   tmp, content_type, field.headers)
                    out.add(field.name, ff)
                else:
                    value = await field.read(decode=True)
                    if content_type is None or \
                            content_type.startswith('text/'):
                        charset = field.get_charset(default='utf-8')
                        value = value.decode(charset)
                    out.add(field.name, value)
                    size += len(value)
                    if 0 < max_size < size:
                        raise ValueError(
                            'Maximum request body size exceeded')

                field = await multipart.next()
        else:
            data = await self.read()
            if data:
                charset = self.charset or 'utf-8'
                out.extend(
                    parse_qsl(
                        data.rstrip().decode(charset),
                        keep_blank_values=True,
                        encoding=charset))

        self._post = MultiDictProxy(out)
        return self._post
