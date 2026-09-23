    def _release(self, key, req, transport, protocol, *, should_close=False):
        if self._closed:
            # acquired connection is already released on connector closing
            return

        acquired = self._acquired[key]
        try:
            acquired.remove(transport)
        except KeyError:  # pragma: no cover
            # this may be result of undetermenistic order of objects
            # finalization due garbage collection.
            pass
        else:
            if self._limit is not None and len(acquired) < self._limit:
                self._release_waiter(key)

        resp = req.response

        if not should_close:
            if self._force_close:
                should_close = True
            elif resp is not None:
                should_close = resp._should_close

        reader = protocol.reader
        if should_close or (reader.output and not reader.output.at_eof()):
            transport.close()
        else:
            conns = self._conns.get(key)
            if conns is None:
                conns = self._conns[key] = []
            conns.append((transport, protocol, self._loop.time()))
            reader.unset_parser()

            self._start_cleanup_task()
