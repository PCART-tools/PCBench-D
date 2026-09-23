    def chunk_iTXt(self, pos, length):
        # international text
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
        try:
            k = k.decode("latin-1", "strict")
            lang = lang.decode("utf-8", "strict")
            tk = tk.decode("utf-8", "strict")
            v = v.decode("utf-8", "strict")
        except UnicodeError:
            return s

        self.im_info[k] = self.im_text[k] = iTXt(v, lang, tk)
        self.check_text_memory(len(v))

        return s
