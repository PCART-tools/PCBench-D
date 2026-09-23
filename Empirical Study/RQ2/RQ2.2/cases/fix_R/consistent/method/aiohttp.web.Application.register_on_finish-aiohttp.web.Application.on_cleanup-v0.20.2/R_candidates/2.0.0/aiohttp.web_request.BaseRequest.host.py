    @reify
    def host(self):
        """Read only property for getting *HOST* header of request.

        Returns str or None if HTTP request has no HOST header.
        """
        return self._message.headers.get(hdrs.HOST)
