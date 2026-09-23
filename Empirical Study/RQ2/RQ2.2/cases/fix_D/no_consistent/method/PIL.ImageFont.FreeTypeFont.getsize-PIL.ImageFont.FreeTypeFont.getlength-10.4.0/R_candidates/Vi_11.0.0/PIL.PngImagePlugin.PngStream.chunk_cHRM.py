    def chunk_cHRM(self, pos: int, length: int) -> bytes:
        # chromaticity, 8 unsigned ints, actual value is scaled by 100,000
        # WP x,y, Red x,y, Green x,y Blue x,y

        assert self.fp is not None
        s = ImageFile._safe_read(self.fp, length)
        raw_vals = struct.unpack(">%dI" % (len(s) // 4), s)
        self.im_info["chromaticity"] = tuple(elt / 100000.0 for elt in raw_vals)
        return s
