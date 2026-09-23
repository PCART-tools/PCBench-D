    async def readline(self):
        """Reads body part by line by line."""
        if self._at_eof:
            return b''

        if self._unread:
            line = self._unread.popleft()
        else:
            line = await self._content.readline()

        if line.startswith(self._boundary):
            # the very last boundary may not come with \r\n,
            # so set single rules for everyone
            sline = line.rstrip(b'\r\n')
            boundary = self._boundary
            last_boundary = self._boundary + b'--'
            # ensure that we read exactly the boundary, not something alike
            if sline == boundary or sline == last_boundary:
                self._at_eof = True
                self._unread.append(line)
                return b''
        else:
            next_line = await self._content.readline()
            if next_line.startswith(self._boundary):
                line = line[:-2]  # strip CRLF but only once
            self._unread.append(next_line)

        return line
