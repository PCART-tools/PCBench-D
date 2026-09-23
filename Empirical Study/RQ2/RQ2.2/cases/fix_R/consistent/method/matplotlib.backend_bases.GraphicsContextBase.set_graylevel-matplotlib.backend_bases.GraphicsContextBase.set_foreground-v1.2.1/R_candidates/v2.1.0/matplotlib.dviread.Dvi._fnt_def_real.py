    def _fnt_def_real(self, k, c, s, d, a, l):
        n = self.file.read(a + l)
        fontname = n[-l:].decode('ascii')
        tfm = _tfmfile(fontname)
        if tfm is None:
            if six.PY2:
                error_class = OSError
            else:
                error_class = FileNotFoundError
            raise error_class("missing font metrics file: %s" % fontname)
        if c != 0 and tfm.checksum != 0 and c != tfm.checksum:
            raise ValueError('tfm checksum mismatch: %s' % n)

        vf = _vffile(fontname)

        self.fonts[k] = DviFont(scale=s, tfm=tfm, texname=n, vf=vf)
