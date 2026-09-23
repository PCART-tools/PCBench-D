    @asyncio.coroutine
    def start(self, message, payload, handler):
        """Start processing of incoming requests.

        It reads request line, request headers and request payload, then
        calls handle_request() method. Subclass has to override
        handle_request(). start() handles various exceptions in request
        or response handling. Connection is being closed always unless
        keep_alive(True) specified.
        """
        loop = self._loop
        handler = handler[0]
        manager = self._manager
        keepalive_timeout = self._keepalive_timeout

        while not self._force_close:
            if self.access_log:
                now = loop.time()

            manager.requests_count += 1
            writer = PayloadWriter(self.writer, loop)
            request = self._request_factory(
                message, payload, self, writer, handler)
            try:
                try:
                    resp = yield from self._request_handler(request)
                except HTTPException as exc:
                    resp = exc
                except asyncio.CancelledError:
                    self.log_debug('Ignored premature client disconnection')
                    break
                except asyncio.TimeoutError:
                    self.log_debug('Request handler timed out.')
                    resp = self.handle_error(request, 504)
                except Exception as exc:
                    resp = self.handle_error(request, 500, exc)

                yield from resp.prepare(request)
                yield from resp.write_eof()

                # notify server about keep-alive
                self._keepalive = resp.keep_alive

                # Restore default state.
                # Should be no-op if server code didn't touch these attributes.
                writer.set_tcp_cork(False)
                writer.set_tcp_nodelay(True)

                # log access
                if self.access_log:
                    self.log_access(message, None, resp, loop.time() - now)

                # check payload
                if not payload.is_eof():
                    lingering_time = self._lingering_time
                    if not self._force_close and lingering_time:
                        self.log_debug(
                            'Start lingering close timer for %s sec.',
                            lingering_time)

                        now = loop.time()
                        end_t = now + lingering_time

                        with suppress(asyncio.TimeoutError):
                            while (not payload.is_eof() and now < end_t):
                                timeout = min(end_t - now, lingering_time)
                                with CeilTimeout(timeout, loop=loop):
                                    # read and ignore
                                    yield from payload.readany()
                                now = loop.time()

                    # if payload still uncompleted
                    if not payload.is_eof() and not self._force_close:
                        self.log_debug('Uncompleted request.')
                        self.close()

            except Exception as exc:
                self.log_exception('Unhandled exception', exc_info=exc)
                self.force_close()
            finally:
                if self.transport is None:
                    self.log_debug('Ignored premature client disconnection.')
                elif not self._force_close:
                    if self._messages:
                        message, payload = self._messages.popleft()
                    else:
                        if self._keepalive and not self._close:
                            # start keep-alive timer
                            if keepalive_timeout is not None:
                                now = self._time_service.loop_time
                                self._keepalive_time = now
                                if self._keepalive_handle is None:
                                    self._keepalive_handle = loop.call_at(
                                        now + keepalive_timeout,
                                        self._process_keepalive)

                            # wait for next request
                            waiter = create_future(loop)
                            self._waiters.append(waiter)
                            try:
                                message, payload = yield from waiter
                            except asyncio.CancelledError:
                                # shutdown process
                                break
                        else:
                            break

        # remove handler, close transport if no handlers left
        if not self._force_close:
            self._request_handlers.remove(handler)
            if not self._request_handlers:
                if self.transport is not None:
                    self.transport.close()
