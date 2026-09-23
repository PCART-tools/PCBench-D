    def feed_data(self, data,
                  SEP=b'\r\n', EMPTY=b'',
                  CONTENT_LENGTH=hdrs.CONTENT_LENGTH,
                  METH_CONNECT=hdrs.METH_CONNECT,
                  SEC_WEBSOCKET_KEY1=hdrs.SEC_WEBSOCKET_KEY1):

        messages = []

        if self._tail:
            data, self._tail = self._tail + data, b''

        data_len = len(data)
        start_pos = 0
        loop = self.loop

        while start_pos < data_len:

            # read HTTP message (request/response line + headers), \r\n\r\n
            # and split by lines
            if self._payload_parser is None and not self._upgraded:
                pos = data.find(SEP, start_pos)
                # consume \r\n
                if pos == start_pos and not self._lines:
                    start_pos = pos + 2
                    continue

                if pos >= start_pos:
                    # line found
                    self._lines.append(data[start_pos:pos])
                    start_pos = pos + 2

                    # \r\n\r\n found
                    if self._lines[-1] == EMPTY:
                        try:
                            msg = self.parse_message(self._lines)
                        finally:
                            self._lines.clear()

                        # payload length
                        length = msg.headers.get(CONTENT_LENGTH)
                        if length is not None:
                            try:
                                length = int(length)
                            except ValueError:
                                raise InvalidHeader(CONTENT_LENGTH)
                            if length < 0:
                                raise InvalidHeader(CONTENT_LENGTH)

                        # do not support old websocket spec
                        if SEC_WEBSOCKET_KEY1 in msg.headers:
                            raise InvalidHeader(SEC_WEBSOCKET_KEY1)

                        self._upgraded = msg.upgrade

                        method = getattr(msg, 'method', self.method)

                        # calculate payload
                        if ((length is not None and length > 0) or
                                msg.chunked and not msg.upgrade):
                            payload = StreamReader(
                                self.protocol, timer=self.timer, loop=loop)
                            payload_parser = HttpPayloadParser(
                                payload, length=length,
                                chunked=msg.chunked, method=method,
                                compression=msg.compression,
                                code=self.code, readall=self.readall,
                                response_with_body=self.response_with_body,
                                auto_decompress=self._auto_decompress)
                            if not payload_parser.done:
                                self._payload_parser = payload_parser
                        elif method == METH_CONNECT:
                            payload = StreamReader(
                                self.protocol, timer=self.timer, loop=loop)
                            self._upgraded = True
                            self._payload_parser = HttpPayloadParser(
                                payload, method=msg.method,
                                compression=msg.compression, readall=True,
                                auto_decompress=self._auto_decompress)
                        else:
                            if (getattr(msg, 'code', 100) >= 199 and
                                    length is None and self.read_until_eof):
                                payload = StreamReader(
                                    self.protocol, timer=self.timer, loop=loop)
                                payload_parser = HttpPayloadParser(
                                    payload, length=length,
                                    chunked=msg.chunked, method=method,
                                    compression=msg.compression,
                                    code=self.code, readall=True,
                                    response_with_body=self.response_with_body,
                                    auto_decompress=self._auto_decompress)
                                if not payload_parser.done:
                                    self._payload_parser = payload_parser
                            else:
                                payload = EMPTY_PAYLOAD

                        messages.append((msg, payload))
                else:
                    self._tail = data[start_pos:]
                    data = EMPTY
                    break

            # no parser, just store
            elif self._payload_parser is None and self._upgraded:
                assert not self._lines
                break

            # feed payload
            elif data and start_pos < data_len:
                assert not self._lines
                try:
                    eof, data = self._payload_parser.feed_data(
                        data[start_pos:])
                except BaseException as exc:
                    if self.payload_exception is not None:
                        self._payload_parser.payload.set_exception(
                            self.payload_exception(str(exc)))
                    else:
                        self._payload_parser.payload.set_exception(exc)

                    eof = True
                    data = b''

                if eof:
                    start_pos = 0
                    data_len = len(data)
                    self._payload_parser = None
                    continue
            else:
                break

        if data and start_pos < data_len:
            data = data[start_pos:]
        else:
            data = EMPTY

        return messages, self._upgraded, data
