    @reify
    def url(self):
        return URL('{}://{}{}'.format(self._scheme,
                                      self._message.headers.get(hdrs.HOST),
                                      str(self._rel_url)))
