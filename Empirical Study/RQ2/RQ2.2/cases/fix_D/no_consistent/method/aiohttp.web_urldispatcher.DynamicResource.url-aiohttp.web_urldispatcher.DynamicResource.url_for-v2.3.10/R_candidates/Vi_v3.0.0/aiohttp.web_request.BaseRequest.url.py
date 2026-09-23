    @reify
    def url(self):
        url = URL.build(scheme=self.scheme, host=self.host)
        return url.join(self._rel_url)
