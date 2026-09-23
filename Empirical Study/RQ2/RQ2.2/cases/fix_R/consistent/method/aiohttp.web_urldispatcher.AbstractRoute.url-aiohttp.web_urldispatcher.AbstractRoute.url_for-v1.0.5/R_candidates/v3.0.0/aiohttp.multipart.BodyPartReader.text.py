    async def text(self, *, encoding=None):
        """Like read(), but assumes that body part contains text data."""
        data = await self.read(decode=True)
        # see https://www.w3.org/TR/html5/forms.html#multipart/form-data-encoding-algorithm # NOQA
        # and https://dvcs.w3.org/hg/xhr/raw-file/tip/Overview.html#dom-xmlhttprequest-send # NOQA
        encoding = encoding or self.get_charset(default='utf-8')
        return data.decode(encoding)
