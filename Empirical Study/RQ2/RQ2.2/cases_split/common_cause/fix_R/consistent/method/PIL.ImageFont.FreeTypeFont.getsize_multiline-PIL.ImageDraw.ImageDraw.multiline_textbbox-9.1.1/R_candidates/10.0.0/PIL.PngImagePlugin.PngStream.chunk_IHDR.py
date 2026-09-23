    def chunk_IHDR(self, pos, length):
        # image header
        s = ImageFile._safe_read(self.fp, length)
        if length < 13:
            if ImageFile.LOAD_TRUNCATED_IMAGES:
                return s
            msg = "Truncated IHDR chunk"
            raise ValueError(msg)
        self.im_size = i32(s, 0), i32(s, 4)
        try:
            self.im_mode, self.im_rawmode = _MODES[(s[8], s[9])]
        except Exception:
            pass
        if s[12]:
            self.im_info["interlace"] = 1
        if s[11]:
            msg = "unknown filter category"
            raise SyntaxError(msg)
        return s
