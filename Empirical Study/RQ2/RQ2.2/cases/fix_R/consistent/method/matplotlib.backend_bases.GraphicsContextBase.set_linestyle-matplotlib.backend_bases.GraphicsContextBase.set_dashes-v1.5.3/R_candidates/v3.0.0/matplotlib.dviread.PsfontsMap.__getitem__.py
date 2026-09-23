    def __getitem__(self, texname):
        assert isinstance(texname, bytes)
        try:
            result = self._font[texname]
        except KeyError:
            fmt = ('A PostScript file for the font whose TeX name is "{0}" '
                   'could not be found in the file "{1}". The dviread module '
                   'can only handle fonts that have an associated PostScript '
                   'font file. '
                   'This problem can often be solved by installing '
                   'a suitable PostScript font package in your (TeX) '
                   'package manager.')
            msg = fmt.format(texname.decode('ascii'), self._filename)
            msg = textwrap.fill(msg, break_on_hyphens=False,
                                break_long_words=False)
            _log.info(msg)
            raise
        fn, enc = result.filename, result.encoding
        if fn is not None and not fn.startswith(b'/'):
            fn = find_tex_file(fn)
        if enc is not None and not enc.startswith(b'/'):
            enc = find_tex_file(result.encoding)
        return result._replace(filename=fn, encoding=enc)
