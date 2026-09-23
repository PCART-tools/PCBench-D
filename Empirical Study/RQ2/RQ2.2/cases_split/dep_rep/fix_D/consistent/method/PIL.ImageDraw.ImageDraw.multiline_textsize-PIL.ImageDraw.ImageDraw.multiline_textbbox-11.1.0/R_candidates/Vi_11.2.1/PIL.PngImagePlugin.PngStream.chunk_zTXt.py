    def chunk_zTXt(self, pos: int, length: int) -> bytes:
        # compressed text
        assert self.fp is not None
        s = ImageFile._safe_read(self.fp, length)
        try:
            k, v = s.split(b"\0", 1)
        except ValueError:
            k = s
            v = b""
        if v:
            comp_method = v[0]
        else:
            comp_method = 0
        if comp_method != 0:
            msg = f"Unknown compression method {comp_method} in zTXt chunk"
            raise SyntaxError(msg)
        try:
            v = _safe_zlib_decompress(v[1:])
        except ValueError:
            if ImageFile.LOAD_TRUNCATED_IMAGES:
                v = b""
            else:
                raise
        except zlib.error:
            v = b""

        if k:
            k_str = k.decode("latin-1", "strict")
            v_str = v.decode("latin-1", "replace")

            self.im_info[k_str] = self.im_text[k_str] = v_str
            self.check_text_memory(len(v_str))

        return s
