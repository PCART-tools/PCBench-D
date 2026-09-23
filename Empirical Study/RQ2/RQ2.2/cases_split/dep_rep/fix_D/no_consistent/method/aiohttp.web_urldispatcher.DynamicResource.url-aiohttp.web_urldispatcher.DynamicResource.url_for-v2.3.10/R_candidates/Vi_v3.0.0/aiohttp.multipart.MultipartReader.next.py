    async def next(self):
        """Emits the next multipart body part."""
        # So, if we're at BOF, we need to skip till the boundary.
        if self._at_eof:
            return
        await self._maybe_release_last_part()
        if self._at_bof:
            await self._read_until_first_boundary()
            self._at_bof = False
        else:
            await self._read_boundary()
        if self._at_eof:  # we just read the last boundary, nothing to do there
            return
        self._last_part = await self.fetch_next_part()
        return self._last_part
