    @asyncio.coroutine
    def readline(self):
        if self._exception is not None:
            raise self._exception

        line = []
        line_size = 0
        not_enough = True

        while not_enough:
            while self._buffer and not_enough:
                offset = self._buffer_offset
                ichar = self._buffer[0].find(b'\n', offset) + 1
                # Read from current offset to found b'\n' or to the end.
                data = self._read_nowait_chunk(ichar - offset if ichar else -1)
                line.append(data)
                line_size += len(data)
                if ichar:
                    not_enough = False

                if line_size > self._limit:
                    raise ValueError('Line is too long')

            if self._eof:
                break

            if not_enough:
                yield from self._wait('readline')

        return b''.join(line)
