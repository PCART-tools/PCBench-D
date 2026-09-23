    def __repr__(self):
        self._request = None
        if self._request is None:
            meth = 'none'
            path = 'none'
        else:
            meth = 'none'
            path = 'none'
            # meth = self._request.method
            # path = self._request.rel_url.raw_path
        return "<{} {}:{} {}>".format(
            self.__class__.__name__, meth, path,
            'connected' if self.transport is not None else 'disconnected')
