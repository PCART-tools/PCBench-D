    async def _resolve_host(self, host, port, traces=None):
        if is_ip_address(host):
            return [{'hostname': host, 'host': host, 'port': port,
                     'family': self._family, 'proto': 0, 'flags': 0}]

        if not self._use_dns_cache:

            if traces:
                for trace in traces:
                    await trace.send_dns_resolvehost_start(host)

            res = (await self._resolver.resolve(
                host, port, family=self._family))

            if traces:
                for trace in traces:
                    await trace.send_dns_resolvehost_end(host)

            return res

        key = (host, port)

        if (key in self._cached_hosts) and \
                (not self._cached_hosts.expired(key)):

            if traces:
                for trace in traces:
                    await trace.send_dns_cache_hit(host)

            return self._cached_hosts.next_addrs(key)

        if key in self._throttle_dns_events:
            if traces:
                for trace in traces:
                    await trace.send_dns_cache_hit(host)
            await self._throttle_dns_events[key].wait()
        else:
            if traces:
                for trace in traces:
                    await trace.send_dns_cache_miss(host)
            self._throttle_dns_events[key] = \
                EventResultOrError(self._loop)
            try:

                if traces:
                    for trace in traces:
                        await trace.send_dns_resolvehost_start(host)

                addrs = await \
                    asyncio.shield(self._resolver.resolve(host,
                                                          port,
                                                          family=self._family),
                                   loop=self._loop)
                if traces:
                    for trace in traces:
                        await trace.send_dns_resolvehost_end(host)

                self._cached_hosts.add(key, addrs)
                self._throttle_dns_events[key].set()
            except BaseException as e:
                # any DNS exception, independently of the implementation
                # is set for the waiters to raise the same exception.
                self._throttle_dns_events[key].set(exc=e)
                raise
            finally:
                self._throttle_dns_events.pop(key)

        return self._cached_hosts.next_addrs(key)
