    def data_received(self, data):
        if self._force_close or self._close:
            return

        # parse http messages
        if self._payload_parser is None and not self._upgrade:
            try:
                messages, upgraded, tail = self._request_parser.feed_data(data)
            except HttpProcessingError as exc:
                # something happened during parsing
                self.close()
                self._error_handler = ensure_future(
                    self.handle_parse_error(
                        PayloadWriter(self.writer, self._loop),
                        400, exc, exc.message),
                    loop=self._loop)
            except Exception as exc:
                # 500: internal error
                self.close()
                self._error_handler = ensure_future(
                    self.handle_parse_error(
                        PayloadWriter(self.writer, self._loop),
                        500, exc), loop=self._loop)
            else:
                for (msg, payload) in messages:
                    self._request_count += 1

                    if self._waiters:
                        waiter = self._waiters.popleft()
                        waiter.set_result((msg, payload))
                    elif self._max_concurrent_handlers:
                        self._max_concurrent_handlers -= 1
                        data = []
                        handler = ensure_future(
                            self.start(msg, payload, data), loop=self._loop)
                        data.append(handler)
                        self._request_handlers.append(handler)
                    else:
                        self._messages.append((msg, payload))

                self._upgraded = upgraded
                if upgraded:
                    self._message_tail = tail

        # no parser, just store
        elif self._payload_parser is None and self._upgrade and data:
            self._message_tail += data

        # feed payload
        elif data:
            eof, tail = self._payload_parser.feed_data(data)
            if eof:
                self.close()
