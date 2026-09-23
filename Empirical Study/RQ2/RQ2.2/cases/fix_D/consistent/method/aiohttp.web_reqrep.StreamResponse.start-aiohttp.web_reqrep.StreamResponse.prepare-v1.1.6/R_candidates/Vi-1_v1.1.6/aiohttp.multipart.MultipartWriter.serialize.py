    def serialize(self):
        """Yields multipart byte chunks."""
        if not self.parts:
            yield b''
            return

        for part in self.parts:
            yield b'--' + self.boundary + b'\r\n'
            yield from part.serialize()
        else:
            yield b'--' + self.boundary + b'--\r\n'

        yield b''
