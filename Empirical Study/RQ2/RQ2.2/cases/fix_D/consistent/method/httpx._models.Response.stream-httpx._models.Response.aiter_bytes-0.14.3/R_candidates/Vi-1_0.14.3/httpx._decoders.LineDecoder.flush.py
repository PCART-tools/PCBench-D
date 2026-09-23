    def flush(self) -> typing.List[str]:
        if self.buffer.endswith("\r"):
            # Handle the case where we had a trailing '\r', which could have
            # been a '\r\n' pair.
            lines = [self.buffer[:-1] + "\n"]
        elif self.buffer:
            lines = [self.buffer]
        else:
            lines = []
        self.buffer = ""
        return lines
