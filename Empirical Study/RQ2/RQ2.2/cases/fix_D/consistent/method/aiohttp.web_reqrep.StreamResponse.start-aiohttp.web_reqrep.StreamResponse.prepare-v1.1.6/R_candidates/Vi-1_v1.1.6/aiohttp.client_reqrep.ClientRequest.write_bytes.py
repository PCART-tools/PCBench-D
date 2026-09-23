    @asyncio.coroutine
    def write_bytes(self, request, reader):
        """Support coroutines that yields bytes objects."""
        # 100 response
        if self._continue is not None:
            yield from self._continue

        try:
            if asyncio.iscoroutine(self.body):
                exc = None
                value = None
                stream = self.body

                while True:
                    try:
                        if exc is not None:
                            result = stream.throw(exc)
                        else:
                            result = stream.send(value)
                    except StopIteration as exc:
                        if isinstance(exc.value, bytes):
                            yield from request.write(exc.value, drain=True)
                        break
                    except:
                        self.response.close()
                        raise

                    if isinstance(result, asyncio.Future):
                        exc = None
                        value = None
                        try:
                            value = yield result
                        except Exception as err:
                            exc = err
                    elif isinstance(result, (bytes, bytearray)):
                        yield from request.write(result, drain=True)
                        value = None
                    else:
                        raise ValueError(
                            'Bytes object is expected, got: %s.' %
                            type(result))

            elif isinstance(self.body, (asyncio.StreamReader,
                                        streams.StreamReader)):
                chunk = yield from self.body.read(streams.DEFAULT_LIMIT)
                while chunk:
                    yield from request.write(chunk, drain=True)
                    chunk = yield from self.body.read(streams.DEFAULT_LIMIT)

            elif isinstance(self.body, streams.DataQueue):
                while True:
                    try:
                        chunk = yield from self.body.read()
                        if not chunk:
                            break
                        yield from request.write(chunk, drain=True)
                    except streams.EofStream:
                        break

            elif isinstance(self.body, io.IOBase):
                chunk = self.body.read(self.chunked)
                while chunk:
                    request.write(chunk)
                    chunk = self.body.read(self.chunked)
            else:
                if isinstance(self.body, (bytes, bytearray)):
                    self.body = (self.body,)

                for chunk in self.body:
                    request.write(chunk)

        except Exception as exc:
            new_exc = aiohttp.ClientRequestError(
                'Can not write request body for %s' % self.url)
            new_exc.__context__ = exc
            new_exc.__cause__ = exc
            reader.set_exception(new_exc)
        else:
            try:
                ret = request.write_eof()
                # NB: in asyncio 3.4.1+ StreamWriter.drain() is coroutine
                # see bug #170
                if (asyncio.iscoroutine(ret) or
                        isinstance(ret, asyncio.Future)):
                    yield from ret
            except Exception as exc:
                new_exc = aiohttp.ClientRequestError(
                    'Can not write request body for %s' % self.url)
                new_exc.__context__ = exc
                new_exc.__cause__ = exc
                reader.set_exception(new_exc)

        self._writer = None
