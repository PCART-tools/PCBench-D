    def chunk_iCCP(self, pos: int, length: int) -> bytes:
        # ICC profile
        assert self.fp is not None
        s = ImageFile._safe_read(self.fp, length)
        # according to PNG spec, the iCCP chunk contains:
        # Profile name  1-79 bytes (character string)
        # Null separator        1 byte (null character)
        # Compression method    1 byte (0)
        # Compressed profile    n bytes (zlib with deflate compression)
        i = s.find(b"\0")
        logger.debug("iCCP profile name %r", s[:i])
        comp_method = s[i + 1]
        logger.debug("Compression method %s", comp_method)
        if comp_method != 0:
            msg = f"Unknown compression method {comp_method} in iCCP chunk"
            raise SyntaxError(msg)
        try:
            icc_profile = _safe_zlib_decompress(s[i + 2 :])
        except ValueError:
            if ImageFile.LOAD_TRUNCATED_IMAGES:
                icc_profile = None
            else:
                raise
        except zlib.error:
            icc_profile = None  # FIXME
        self.im_info["icc_profile"] = icc_profile
        return s
