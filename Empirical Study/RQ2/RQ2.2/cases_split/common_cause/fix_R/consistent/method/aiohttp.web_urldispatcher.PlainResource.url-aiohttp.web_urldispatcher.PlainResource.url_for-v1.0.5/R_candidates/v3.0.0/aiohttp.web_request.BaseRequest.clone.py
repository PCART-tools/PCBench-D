    def clone(self, *, method=sentinel, rel_url=sentinel,
              headers=sentinel, scheme=sentinel, host=sentinel,
              remote=sentinel):
        """Clone itself with replacement some attributes.

        Creates and returns a new instance of Request object. If no parameters
        are given, an exact copy is returned. If a parameter is not passed, it
        will reuse the one from the current request object.

        """

        if self._read_bytes:
            raise RuntimeError("Cannot clone request "
                               "after reading it's content")

        dct = {}
        if method is not sentinel:
            dct['method'] = method
        if rel_url is not sentinel:
            rel_url = URL(rel_url)
            dct['url'] = rel_url
            dct['path'] = str(rel_url)
        if headers is not sentinel:
            dct['headers'] = CIMultiDict(headers)
            dct['raw_headers'] = tuple((k.encode('utf-8'), v.encode('utf-8'))
                                       for k, v in headers.items())

        message = self._message._replace(**dct)

        kwargs = {}
        if scheme is not sentinel:
            kwargs['scheme'] = scheme
        if host is not sentinel:
            kwargs['host'] = host
        if remote is not sentinel:
            kwargs['remote'] = remote

        return self.__class__(
            message,
            self._payload,
            self._protocol,
            self._payload_writer,
            self._task,
            self._loop,
            client_max_size=self._client_max_size,
            state=self._state.copy(),
            **kwargs)
