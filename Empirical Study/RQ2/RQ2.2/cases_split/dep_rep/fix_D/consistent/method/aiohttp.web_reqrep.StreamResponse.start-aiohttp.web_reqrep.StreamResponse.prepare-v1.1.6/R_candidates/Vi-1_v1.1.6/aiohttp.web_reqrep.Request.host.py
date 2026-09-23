    @reify
    def host(self):
        """Read only property for getting *HOST* header of request.

        Returns str or None if HTTP request has no HOST header.
        """
        warnings.warn("host property is deprecated, "
                      "use .url.host instead",
                      DeprecationWarning)
        return self._message.headers.get(hdrs.HOST)
