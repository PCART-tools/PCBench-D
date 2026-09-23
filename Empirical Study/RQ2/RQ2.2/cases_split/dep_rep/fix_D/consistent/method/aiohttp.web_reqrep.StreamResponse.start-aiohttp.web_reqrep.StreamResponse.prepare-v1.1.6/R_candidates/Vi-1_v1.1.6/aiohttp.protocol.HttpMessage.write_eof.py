    def write_eof(self):
        self.write(EOF_MARKER)
        try:
            self.writer.throw(aiohttp.EofStream())
        except StopIteration:
            pass

        return self.transport.drain()
