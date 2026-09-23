    @asyncio.coroutine
    def write_bytes(self, writer, conn):
        """Support coroutines that yields bytes objects."""
        # 100 response
        if self._continue is not None:
            yield from writer.drain()
            yield from self._continue

        try:
            if isinstance(self.body, payload.Payload):
                yield from self.body.write(writer)
            else:
                if isinstance(self.body, (bytes, bytearray)):
                    self.body = (self.body,)

                for chunk in self.body:
                    writer.write(chunk)

            yield from writer.write_eof()
        except OSError as exc:
            new_exc = ClientOSError(
                exc.errno,
                'Can not write request body for %s' % self.url)
            new_exc.__context__ = exc
            new_exc.__cause__ = exc
            conn.protocol.set_exception(new_exc)
        except asyncio.CancelledError as exc:
            if not conn.closed:
                conn.protocol.set_exception(exc)
        except Exception as exc:
            conn.protocol.set_exception(exc)
        finally:
            self._writer = None
