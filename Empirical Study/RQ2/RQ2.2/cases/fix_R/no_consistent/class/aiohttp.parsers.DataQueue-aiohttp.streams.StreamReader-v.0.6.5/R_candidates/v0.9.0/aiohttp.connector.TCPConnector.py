class TCPConnector(BaseConnector):

    def __init__(self, *args, verify_ssl=True,
                 resolve=False, family=socket.AF_INET, **kwargs):
        super().__init__(*args, **kwargs)

        self._verify_ssl = verify_ssl
        self._family = family
        self._resolve = resolve
        self._resolved_hosts = {}

    @property
    def verify_ssl(self):
        """Do check for ssl certifications?"""
        return self._verify_ssl

    @property
    def family(self):
        """Socket family like AF_INET"""
        return self._family

    @property
    def resolve(self):
        """Do DNS lookup for host name?"""
        return self._resolve

    @property
    def resolved_hosts(self):
        """The dict of (host, port) -> (ipaddr, port) pairs"""
        return dict(self._resolved_hosts)

    def clear_resolved_hosts(self, host=None, port=None):
        if host is not None and port is not None:
            key = (host, port)
            if key in self._resolved_hosts:
                del self._resolved_hosts[key]
        else:
            self._resolved_hosts.clear()

    @asyncio.coroutine
    def _resolve_host(self, host, port):
        if self._resolve:
            key = (host, port)

            if key not in self._resolved_hosts:
                infos = yield from self._loop.getaddrinfo(
                    host, port, type=socket.SOCK_STREAM, family=self._family)

                hosts = []
                for family, _, proto, _, address in infos:
                    hosts.append(
                        {'hostname': host,
                         'host': address[0], 'port': address[1],
                         'family': family, 'proto': proto,
                         'flags': socket.AI_NUMERICHOST})
                self._resolved_hosts[key] = hosts

            return list(self._resolved_hosts[key])
        else:
            return [{'hostname': host, 'host': host, 'port': port,
                     'family': self._family, 'proto': 0, 'flags': 0}]

    def _create_connection(self, req, **kwargs):
        """Create connection. Has same keyword arguments
        as BaseEventLoop.create_connection
        """
        sslcontext = req.ssl
        if req.ssl and not self._verify_ssl:
            sslcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            sslcontext.options |= ssl.OP_NO_SSLv2
            sslcontext.set_default_verify_paths()

        hosts = yield from self._resolve_host(req.host, req.port)

        while hosts:
            hinfo = hosts.pop()
            try:
                return (yield from self._loop.create_connection(
                    self._factory, hinfo['host'], hinfo['port'],
                    ssl=sslcontext, family=hinfo['family'],
                    proto=hinfo['proto'], flags=hinfo['flags'],
                    server_hostname=hinfo['hostname'] if sslcontext else None,
                    **kwargs))
            except OSError:
                if not hosts:
                    raise
