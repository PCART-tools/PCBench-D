    def _read_until(self, terminator):
        """Read until the prompt is reached."""
        buf = bytearray()
        while True:
            c = self._proc.stdout.read(1)
            if not c:
                raise _ConverterError
            buf.extend(c)
            if buf.endswith(terminator):
                return bytes(buf)
