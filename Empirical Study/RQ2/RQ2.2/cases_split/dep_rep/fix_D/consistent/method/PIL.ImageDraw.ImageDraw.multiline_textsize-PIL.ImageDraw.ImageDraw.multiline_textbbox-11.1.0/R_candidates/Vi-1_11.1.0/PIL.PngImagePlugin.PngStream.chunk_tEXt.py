    def chunk_tEXt(self, pos: int, length: int) -> bytes:
        # text
        assert self.fp is not None
        s = ImageFile._safe_read(self.fp, length)
        try:
            k, v = s.split(b"\0", 1)
        except ValueError:
            # fallback for broken tEXt tags
            k = s
            v = b""
        if k:
            k_str = k.decode("latin-1", "strict")
            v_str = v.decode("latin-1", "replace")

            self.im_info[k_str] = v if k == b"exif" else v_str
            self.im_text[k_str] = v_str
            self.check_text_memory(len(v_str))

        return s
