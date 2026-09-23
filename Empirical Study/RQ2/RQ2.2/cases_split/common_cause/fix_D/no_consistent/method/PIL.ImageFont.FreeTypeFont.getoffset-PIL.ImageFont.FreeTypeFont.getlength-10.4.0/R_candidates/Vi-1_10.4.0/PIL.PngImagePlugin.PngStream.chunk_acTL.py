    def chunk_acTL(self, pos: int, length: int) -> bytes:
        s = ImageFile._safe_read(self.fp, length)
        if length < 8:
            if ImageFile.LOAD_TRUNCATED_IMAGES:
                return s
            msg = "APNG contains truncated acTL chunk"
            raise ValueError(msg)
        if self.im_n_frames is not None:
            self.im_n_frames = None
            warnings.warn("Invalid APNG, will use default PNG image if possible")
            return s
        n_frames = i32(s)
        if n_frames == 0 or n_frames > 0x80000000:
            warnings.warn("Invalid APNG, will use default PNG image if possible")
            return s
        self.im_n_frames = n_frames
        self.im_info["loop"] = i32(s, 4)
        self.im_custom_mimetype = "image/apng"
        return s
