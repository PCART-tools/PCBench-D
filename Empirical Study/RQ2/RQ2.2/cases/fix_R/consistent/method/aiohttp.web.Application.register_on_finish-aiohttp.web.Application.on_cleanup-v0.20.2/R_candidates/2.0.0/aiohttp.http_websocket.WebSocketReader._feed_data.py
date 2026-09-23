    def _feed_data(self, data):
        for fin, opcode, payload in self.parse_frame(data):
            if opcode == WSMsgType.CLOSE:
                if len(payload) >= 2:
                    close_code = UNPACK_CLOSE_CODE(payload[:2])[0]
                    if (close_code < 3000 and
                            close_code not in ALLOWED_CLOSE_CODES):
                        raise WebSocketError(
                            WSCloseCode.PROTOCOL_ERROR,
                            'Invalid close code: {}'.format(close_code))
                    try:
                        close_message = payload[2:].decode('utf-8')
                    except UnicodeDecodeError as exc:
                        raise WebSocketError(
                            WSCloseCode.INVALID_TEXT,
                            'Invalid UTF-8 text message') from exc
                    msg = WSMessage(WSMsgType.CLOSE, close_code, close_message)
                elif payload:
                    raise WebSocketError(
                        WSCloseCode.PROTOCOL_ERROR,
                        'Invalid close frame: {} {} {!r}'.format(
                            fin, opcode, payload))
                else:
                    msg = WSMessage(WSMsgType.CLOSE, 0, '')

                self.queue.feed_data(msg, 0)

            elif opcode == WSMsgType.PING:
                self.queue.feed_data(
                    WSMessage(WSMsgType.PING, payload, ''), len(payload))

            elif opcode == WSMsgType.PONG:
                self.queue.feed_data(
                    WSMessage(WSMsgType.PONG, payload, ''), len(payload))

            elif opcode not in (
                    WSMsgType.TEXT, WSMsgType.BINARY) and not self._opcode:
                raise WebSocketError(
                    WSCloseCode.PROTOCOL_ERROR,
                    "Unexpected opcode={!r}".format(opcode))
            else:
                # load text/binary

                if not fin:
                    # got partial frame payload
                    if opcode != WSMsgType.CONTINUATION:
                        self._opcode = opcode
                    self._partial.append(payload)
                else:
                    # previous frame was non finished
                    # we should get continuation opcode
                    if self._partial:
                        if opcode != WSMsgType.CONTINUATION:
                            raise WebSocketError(
                                WSCloseCode.PROTOCOL_ERROR,
                                'The opcode in non-fin frame is expected '
                                'to be zero, got {!r}'.format(opcode))

                    if opcode == WSMsgType.CONTINUATION:
                        opcode = self._opcode

                    self._partial.append(payload)

                    if opcode == WSMsgType.TEXT:
                        try:
                            text = b''.join(self._partial).decode('utf-8')
                            self.queue.feed_data(
                                WSMessage(WSMsgType.TEXT, text, ''), len(text))
                        except UnicodeDecodeError as exc:
                            raise WebSocketError(
                                WSCloseCode.INVALID_TEXT,
                                'Invalid UTF-8 text message') from exc
                    else:
                        data = b''.join(self._partial)
                        self.queue.feed_data(
                            WSMessage(WSMsgType.BINARY, data, ''), len(data))

                    self._start_opcode = None
                    self._partial.clear()

        return False, b''
