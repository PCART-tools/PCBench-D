    def _fnt_def_real(self, k, c, s, d, a, l):
        n = self.file.read(a + l)
        fontname = n[-l:].decode('ascii')
        try:
            tfm = _tfmfile(fontname)
        except FileNotFoundError as exc:
            # Explicitly allow defining missing fonts for Vf support; we only
            # register an error when trying to load a glyph from a missing font
            # and throw that error in Dvi._read.  For Vf, _finalize_packet
            # checks whether a missing glyph has been used, and in that case
            # skips the glyph definition.
            self.fonts[k] = cbook._ExceptionInfo.from_exception(exc)
            return
        if c != 0 and tfm.checksum != 0 and c != tfm.checksum:
            raise ValueError(f'tfm checksum mismatch: {n}')
        try:
            vf = _vffile(fontname)
        except FileNotFoundError:
            vf = None
        self.fonts[k] = DviFont(scale=s, tfm=tfm, texname=n, vf=vf)
