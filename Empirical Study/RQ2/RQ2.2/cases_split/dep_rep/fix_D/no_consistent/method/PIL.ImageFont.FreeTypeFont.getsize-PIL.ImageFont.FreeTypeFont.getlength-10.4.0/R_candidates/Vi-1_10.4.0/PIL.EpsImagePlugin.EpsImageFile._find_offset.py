    def _find_offset(self, fp):
        s = fp.read(4)

        if s == b"%!PS":
            # for HEAD without binary preview
            fp.seek(0, io.SEEK_END)
            length = fp.tell()
            offset = 0
        elif i32(s) == 0xC6D3D0C5:
            # FIX for: Some EPS file not handled correctly / issue #302
            # EPS can contain binary data
            # or start directly with latin coding
            # more info see:
            # https://web.archive.org/web/20160528181353/http://partners.adobe.com/public/developer/en/ps/5002.EPSF_Spec.pdf
            s = fp.read(8)
            offset = i32(s)
            length = i32(s, 4)
        else:
            msg = "not an EPS file"
            raise SyntaxError(msg)

        return length, offset
