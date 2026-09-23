    def data_received(self, data):
        if not data:
            return

        # custom payload parser
        if self._payload_parser is not None:
            eof, tail = self._payload_parser.feed_data(data)
            if eof:
                self._payload = None
                self._payload_parser = None

                if tail:
                    self.data_received(tail)
            return
        else:
            if self._upgraded or self._parser is None:
                # i.e. websocket connection, websocket parser is not set yet
                self._tail += data
            else:
                # parse http messages
                try:
                    messages, upgraded, tail = self._parser.feed_data(data)
                except BaseException as exc:
                    self._should_close = True
                    self.transport.close()
                    self.set_exception(exc)
                    return

                self._upgraded = upgraded

                for message, payload in messages:
                    if message.should_close:
                        self._should_close = True

                    self._message = message
                    self._payload = payload

                    if (self._skip_payload or
                            message.code in self._skip_status_codes):
                        self.feed_data((message, EMPTY_PAYLOAD), 0)
                    else:
                        self.feed_data((message, payload), 0)

                if tail:
                    if upgraded:
                        self.data_received(tail)
                    else:
                        self._tail = tail
