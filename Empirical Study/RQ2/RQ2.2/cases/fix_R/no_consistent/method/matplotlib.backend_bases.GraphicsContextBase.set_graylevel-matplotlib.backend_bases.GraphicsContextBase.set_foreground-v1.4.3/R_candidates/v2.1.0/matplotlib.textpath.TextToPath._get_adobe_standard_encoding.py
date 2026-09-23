    def _get_adobe_standard_encoding(self):
        enc_name = dviread.find_tex_file('8a.enc')
        enc = dviread.Encoding(enc_name)
        return {c: i for i, c in enumerate(enc.encoding)}
