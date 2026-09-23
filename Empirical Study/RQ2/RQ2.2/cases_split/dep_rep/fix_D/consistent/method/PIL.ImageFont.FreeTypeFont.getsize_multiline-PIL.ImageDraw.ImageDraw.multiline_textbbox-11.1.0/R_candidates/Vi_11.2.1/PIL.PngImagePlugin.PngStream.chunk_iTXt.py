    def chunk_iTXt(self, pos: int, length: int) -> bytes:
        # international text
        assert self.fp is not None
        r = s = ImageFile._safe_read(self.fp, length)
        try:
            k, r = r.split(b"\0", 1)
        except ValueError:
            return s
        if len(r) < 2:
            return s
        cf, cm, r = r[0], r[1], r[2:]
        try:
            lang, tk, v = r.split(b"\0", 2)
        except ValueError:
            return s
        if cf != 0:
            if cm == 0:
                try:
                    v = _safe_zlib_decompress(v)
                except ValueError:
                    if ImageFile.LOAD_TRUNCATED_IMAGES:
                        return s
                    else:
                        raise
                except zlib.error:
                    return s
            else:
                return s
        if k == b"XML:com.adobe.xmp":
            self.im_info["xmp"] = v
        try:
            k_str = k.decode("latin-1", "strict")
            lang_str = lang.decode("utf-8", "strict")
            tk_str = tk.decode("utf-8", "strict")
            v_str = v.decode("utf-8", "strict")
        except UnicodeError:
            return s

        self.im_info[k_str] = self.im_text[k_str] = iTXt(v_str, lang_str, tk_str)
        self.check_text_memory(len(v_str))

        return s
