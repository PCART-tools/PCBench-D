    @asyncio.coroutine
    def text(self, *, encoding=None):
        """Like :meth:`read`, but assumes that body part contains text data.

        :param str encoding: Custom text encoding. Overrides specified
                             in charset param of `Content-Type` header

        :rtype: str
        """
        data = yield from self.read(decode=True)
        encoding = encoding or self.get_charset(default='latin1')
        return data.decode(encoding)
