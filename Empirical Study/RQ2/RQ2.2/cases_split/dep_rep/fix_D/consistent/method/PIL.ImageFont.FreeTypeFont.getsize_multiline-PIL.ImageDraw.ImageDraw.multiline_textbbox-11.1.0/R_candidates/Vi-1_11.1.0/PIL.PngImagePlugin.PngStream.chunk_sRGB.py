    def chunk_sRGB(self, pos: int, length: int) -> bytes:
        # srgb rendering intent, 1 byte
        # 0 perceptual
        # 1 relative colorimetric
        # 2 saturation
        # 3 absolute colorimetric

        assert self.fp is not None
        s = ImageFile._safe_read(self.fp, length)
        if length < 1:
            if ImageFile.LOAD_TRUNCATED_IMAGES:
                return s
            msg = "Truncated sRGB chunk"
            raise ValueError(msg)
        self.im_info["srgb"] = s[0]
        return s
