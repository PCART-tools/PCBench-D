    def read(self):
        """Fetch a new chunk. Returns header information."""
        cid = None

        if self.queue:
            cid, pos, length = self.queue.pop()
            self.fp.seek(pos)
        else:
            s = self.fp.read(8)
            cid = s[4:]
            pos = self.fp.tell()
            length = i32(s)

        if not is_cid(cid):
            if not ImageFile.LOAD_TRUNCATED_IMAGES:
                msg = f"broken PNG file (chunk {repr(cid)})"
                raise SyntaxError(msg)

        return cid, pos, length
