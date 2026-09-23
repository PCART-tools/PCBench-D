    def wait_for(self, terminator):
        """Read until the terminator is reached."""
        buf = ''
        while True:
            c = self.stdout.read(1)
            if not c:
                raise RuntimeError(
                    f'Subprocess died before emitting expected {terminator!r}')
            buf += c
            if buf.endswith(terminator):
                return
