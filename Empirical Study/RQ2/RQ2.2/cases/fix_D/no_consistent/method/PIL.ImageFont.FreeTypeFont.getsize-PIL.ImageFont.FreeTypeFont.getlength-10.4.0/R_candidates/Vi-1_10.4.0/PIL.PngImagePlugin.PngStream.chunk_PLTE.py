    def chunk_PLTE(self, pos: int, length: int) -> bytes:
        # palette
        s = ImageFile._safe_read(self.fp, length)
        if self.im_mode == "P":
            self.im_palette = "RGB", s
        return s
