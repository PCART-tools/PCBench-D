    async def _read_boundary(self):
        chunk = (await self._readline()).rstrip()
        if chunk == self._boundary:
            pass
        elif chunk == self._boundary + b'--':
            self._at_eof = True
            epilogue = await self._readline()
            next_line = await self._readline()

            # the epilogue is expected and then either the end of input or the
            # parent multipart boundary, if the parent boundary is found then
            # it should be marked as unread and handed to the parent for
            # processing
            if next_line[:2] == b'--':
                self._unread.append(next_line)
            # otherwise the request is likely missing an epilogue and both
            # lines should be passed to the parent for processing
            # (this handles the old behavior gracefully)
            else:
                self._unread.extend([next_line, epilogue])
        else:
            raise ValueError('Invalid boundary %r, expected %r'
                             % (chunk, self._boundary))
