    def chunk_pHYs(self, pos: int, length: int) -> bytes:
        # pixels per unit
        assert self.fp is not None
        s = ImageFile._safe_read(self.fp, length)
        if length < 9:
            if ImageFile.LOAD_TRUNCATED_IMAGES:
                return s
            msg = "Truncated pHYs chunk"
            raise ValueError(msg)
        px, py = i32(s, 0), i32(s, 4)
        unit = s[8]
        if unit == 1:  # meter
            dpi = px * 0.0254, py * 0.0254
            self.im_info["dpi"] = dpi
        elif unit == 0:
            self.im_info["aspect"] = px, py
        return s
