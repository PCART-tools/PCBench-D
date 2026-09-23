    def chunk_fdAT(self, pos, length):
        if length < 4:
            if ImageFile.LOAD_TRUNCATED_IMAGES:
                s = ImageFile._safe_read(self.fp, length)
                return s
            msg = "APNG contains truncated fDAT chunk"
            raise ValueError(msg)
        s = ImageFile._safe_read(self.fp, 4)
        seq = i32(s)
        if self._seq_num != seq - 1:
            msg = "APNG contains frame sequence errors"
            raise SyntaxError(msg)
        self._seq_num = seq
        return self.chunk_IDAT(pos + 4, length - 4)
