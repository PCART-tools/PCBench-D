    def _fnt_def_real(self, k, c, s, d, a, l):
        n = self.file.read(a + l)
        fontname = n[-l:].decode('ascii')
        tfm = _tfmfile(fontname)
        if tfm is None:
            raise FileNotFoundError("missing font metrics file: %s" % fontname)
        if c != 0 and tfm.checksum != 0 and c != tfm.checksum:
            raise ValueError('tfm checksum mismatch: %s' % n)

        vf = _vffile(fontname)

        self.fonts[k] = DviFont(scale=s, tfm=tfm, texname=n, vf=vf)
