    @asyncio.coroutine
    def text(self, *, encoding=None):
        """Like :meth:`read`, but assumes that body part contains text data.

        :param str encoding: Custom text encoding. Overrides specified
                             in charset param of `Content-Type` header

        :rtype: str
        """
        data = yield from self.read(decode=True)
        # see https://www.w3.org/TR/html5/forms.html#multipart/form-data-encoding-algorithm # NOQA
        # and https://dvcs.w3.org/hg/xhr/raw-file/tip/Overview.html#dom-xmlhttprequest-send # NOQA
        encoding = encoding or self.get_charset(default='utf-8')
        return data.decode(encoding)
