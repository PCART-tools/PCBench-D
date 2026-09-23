    def write(self, chunk, *,
              drain=False, EOF_MARKER=EOF_MARKER, EOL_MARKER=EOL_MARKER):
        """Writes chunk of data to a stream by using different writers.

        writer uses filter to modify chunk of data.
        write_eof() indicates end of stream.
        writer can't be used after write_eof() method being called.
        write() return drain future.
        """
        assert (isinstance(chunk, (bytes, bytearray)) or
                chunk is EOF_MARKER), chunk

        size = self.output_length

        if self._send_headers and not self.headers_sent:
            self.send_headers()

        assert self.writer is not None, 'send_headers() is not called.'

        if self.filter:
            chunk = self.filter.send(chunk)
            while chunk not in (EOF_MARKER, EOL_MARKER):
                if chunk:
                    self.writer.send(chunk)
                chunk = next(self.filter)
        else:
            if chunk is not EOF_MARKER:
                self.writer.send(chunk)

        self._output_size += self.output_length - size

        if self._output_size > 64 * 1024:
            if drain:
                self._output_size = 0
                return self.transport.drain()

        return ()
