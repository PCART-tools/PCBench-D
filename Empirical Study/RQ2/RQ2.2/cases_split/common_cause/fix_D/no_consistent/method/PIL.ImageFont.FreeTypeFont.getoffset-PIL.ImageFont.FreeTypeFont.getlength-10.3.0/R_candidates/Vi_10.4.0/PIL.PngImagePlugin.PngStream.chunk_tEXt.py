    def chunk_tEXt(self, pos: int, length: int) -> bytes:
        # text
        s = ImageFile._safe_read(self.fp, length)
        try:
            k, v = s.split(b"\0", 1)
        except ValueError:
            # fallback for broken tEXt tags
            k = s
            v = b""
        if k:
            k = k.decode("latin-1", "strict")
            v_str = v.decode("latin-1", "replace")

            self.im_info[k] = v if k == "exif" else v_str
            self.im_text[k] = v_str
            self.check_text_memory(len(v_str))

        return s
