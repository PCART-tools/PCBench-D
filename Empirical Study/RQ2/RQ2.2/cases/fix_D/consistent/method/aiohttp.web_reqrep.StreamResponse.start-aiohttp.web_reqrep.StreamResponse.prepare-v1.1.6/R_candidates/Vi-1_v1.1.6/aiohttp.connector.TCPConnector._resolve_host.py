    @asyncio.coroutine
    def _resolve_host(self, host, port):
        if is_ip_address(host):
            return [{'hostname': host, 'host': host, 'port': port,
                     'family': self._family, 'proto': 0, 'flags': 0}]

        if self._use_dns_cache:
            key = (host, port)

            if key not in self._cached_hosts:
                self._cached_hosts[key] = yield from \
                    self._resolver.resolve(host, port, family=self._family)

            return self._cached_hosts[key]
        else:
            res = yield from self._resolver.resolve(
                host, port, family=self._family)
            return res
