    @reify
    def rel_url(self):
        return URL(self._message.path)
