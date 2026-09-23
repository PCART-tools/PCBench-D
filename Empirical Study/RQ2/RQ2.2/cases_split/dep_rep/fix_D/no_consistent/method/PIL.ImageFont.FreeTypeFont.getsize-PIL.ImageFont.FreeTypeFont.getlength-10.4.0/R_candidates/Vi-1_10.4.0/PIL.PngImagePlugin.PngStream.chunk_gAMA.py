    def chunk_gAMA(self, pos: int, length: int) -> bytes:
        # gamma setting
        s = ImageFile._safe_read(self.fp, length)
        self.im_info["gamma"] = i32(s) / 100000.0
        return s
