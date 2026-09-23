    @asyncio.coroutine
    def start(self):
        """Start processing of incoming requests.

        It reads request line, request headers and request payload, then
        calls handle_request() method. Subclass has to override
        handle_request(). start() handles various exceptions in request
        or response handling. Connection is being closed always unless
        keep_alive(True) specified.
        """
        reader = self.reader
        self.writer.set_tcp_nodelay(True)

        try:
            while not self._closing:
                message = None
                self._keepalive = False
                self._request_count += 1
                self._reading_request = False

                payload = None
                with Timeout(max(self._slow_request_timeout,
                                 self._keepalive_timeout),
                             loop=self._loop):
                    # read HTTP request method
                    prefix = reader.set_parser(self._request_prefix)
                    yield from prefix.read()

                    # start reading request
                    self._reading_request = True

                    # start slow request timer
                    # read request headers
                    httpstream = reader.set_parser(self._request_parser)
                    message = yield from httpstream.read()

                # request may not have payload
                try:
                    content_length = int(
                        message.headers.get(hdrs.CONTENT_LENGTH, 0))
                except ValueError:
                    raise errors.InvalidHeader(hdrs.CONTENT_LENGTH) from None

                if (content_length > 0 or
                    message.method == 'CONNECT' or
                    hdrs.SEC_WEBSOCKET_KEY1 in message.headers or
                    'chunked' in message.headers.get(
                        hdrs.TRANSFER_ENCODING, '')):
                    payload = streams.FlowControlStreamReader(
                        reader, loop=self._loop)
                    reader.set_parser(
                        aiohttp.HttpPayloadParser(message), payload)
                else:
                    payload = EMPTY_PAYLOAD

                yield from self.handle_request(message, payload)

                if payload and not payload.is_eof():
                    self.log_debug('Uncompleted request.')
                    self._closing = True
                else:
                    reader.unset_parser()
                    if not self._keepalive or not self._keepalive_timeout:
                        self._closing = True

        except asyncio.CancelledError:
            self.log_debug(
                'Request handler cancelled.')
            return
        except asyncio.TimeoutError:
            self.log_debug(
                'Request handler timed out.')
            return
        except errors.ClientDisconnectedError:
            self.log_debug(
                'Ignored premature client disconnection #1.')
            return
        except errors.HttpProcessingError as exc:
            yield from self.handle_error(exc.code, message,
                                         None, exc, exc.headers,
                                         exc.message)
        except Exception as exc:
            yield from self.handle_error(500, message, None, exc)
        finally:
            self._request_handler = None
            if self.transport is None:
                self.log_debug(
                    'Ignored premature client disconnection #2.')
            else:
                self.transport.close()
