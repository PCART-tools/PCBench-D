    def chunk_tRNS(self, pos, length):
        # transparency
        s = ImageFile._safe_read(self.fp, length)
        if self.im_mode == "P":
            if _simple_palette.match(s):
                # tRNS contains only one full-transparent entry,
                # other entries are full opaque
                i = s.find(b"\0")
                if i >= 0:
                    self.im_info["transparency"] = i
            else:
                # otherwise, we have a byte string with one alpha value
                # for each palette entry
                self.im_info["transparency"] = s
        elif self.im_mode in ("1", "L", "I"):
            self.im_info["transparency"] = i16(s)
        elif self.im_mode == "RGB":
            self.im_info["transparency"] = i16(s), i16(s, 2), i16(s, 4)
        return s
