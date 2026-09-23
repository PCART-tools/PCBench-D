    async def form(self, *, encoding=None):
        """Like read(), but assumes that body parts contains form
        urlencoded data.
        """
        data = await self.read(decode=True)
        if not data:
            return None
        encoding = encoding or self.get_charset(default='utf-8')
        return parse_qsl(data.rstrip().decode(encoding),
                         keep_blank_values=True,
                         encoding=encoding)
