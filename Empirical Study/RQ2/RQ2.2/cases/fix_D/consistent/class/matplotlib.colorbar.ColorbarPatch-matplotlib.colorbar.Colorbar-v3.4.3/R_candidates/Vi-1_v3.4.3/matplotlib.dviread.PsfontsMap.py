class PsfontsMap:
    """
    A psfonts.map formatted file, mapping TeX fonts to PS fonts.

    Parameters
    ----------
    filename : str or path-like

    Notes
    -----
    For historical reasons, TeX knows many Type-1 fonts by different
    names than the outside world. (For one thing, the names have to
    fit in eight characters.) Also, TeX's native fonts are not Type-1
    but Metafont, which is nontrivial to convert to PostScript except
    as a bitmap. While high-quality conversions to Type-1 format exist
    and are shipped with modern TeX distributions, we need to know
    which Type-1 fonts are the counterparts of which native fonts. For
    these reasons a mapping is needed from internal font names to font
    file names.

    A texmf tree typically includes mapping files called e.g.
    :file:`psfonts.map`, :file:`pdftex.map`, or :file:`dvipdfm.map`.
    The file :file:`psfonts.map` is used by :program:`dvips`,
    :file:`pdftex.map` by :program:`pdfTeX`, and :file:`dvipdfm.map`
    by :program:`dvipdfm`. :file:`psfonts.map` might avoid embedding
    the 35 PostScript fonts (i.e., have no filename for them, as in
    the Times-Bold example above), while the pdf-related files perhaps
    only avoid the "Base 14" pdf fonts. But the user may have
    configured these files differently.

    Examples
    --------
    >>> map = PsfontsMap(find_tex_file('pdftex.map'))
    >>> entry = map[b'ptmbo8r']
    >>> entry.texname
    b'ptmbo8r'
    >>> entry.psname
    b'Times-Bold'
    >>> entry.encoding
    '/usr/local/texlive/2008/texmf-dist/fonts/enc/dvips/base/8r.enc'
    >>> entry.effects
    {'slant': 0.16700000000000001}
    >>> entry.filename
    """
    __slots__ = ('_font', '_filename')

    # Create a filename -> PsfontsMap cache, so that calling
    # `PsfontsMap(filename)` with the same filename a second time immediately
    # returns the same object.
    @lru_cache()
    def __new__(cls, filename):
        self = object.__new__(cls)
        self._font = {}
        self._filename = os.fsdecode(filename)
        with open(filename, 'rb') as file:
            self._parse(file)
        return self

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

    def _parse(self, file):
        """
        Parse the font mapping file.

        The format is, AFAIK: texname fontname [effects and filenames]
        Effects are PostScript snippets like ".177 SlantFont",
        filenames begin with one or two less-than signs. A filename
        ending in enc is an encoding file, other filenames are font
        files. This can be overridden with a left bracket: <[foobar
        indicates an encoding file named foobar.

        There is some difference between <foo.pfb and <<bar.pfb in
        subsetting, but I have no example of << in my TeX installation.
        """
        # If the map file specifies multiple encodings for a font, we
        # follow pdfTeX in choosing the last one specified. Such
        # entries are probably mistakes but they have occurred.
        # http://tex.stackexchange.com/questions/10826/
        # http://article.gmane.org/gmane.comp.tex.pdftex/4914

        empty_re = re.compile(br'%|\s*$')
        word_re = re.compile(
            br'''(?x) (?:
                 "<\[ (?P<enc1>  [^"]+    )" | # quoted encoding marked by [
                 "<   (?P<enc2>  [^"]+.enc)" | # quoted encoding, ends in .enc
                 "<<? (?P<file1> [^"]+    )" | # quoted font file name
                 "    (?P<eff1>  [^"]+    )" | # quoted effects or font name
                 <\[  (?P<enc3>  \S+      )  | # encoding marked by [
                 <    (?P<enc4>  \S+  .enc)  | # encoding, ends in .enc
                 <<?  (?P<file2> \S+      )  | # font file name
                      (?P<eff2>  \S+      )    # effects or font name
            )''')
        effects_re = re.compile(
            br'''(?x) (?P<slant> -?[0-9]*(?:\.[0-9]+)) \s* SlantFont
                    | (?P<extend>-?[0-9]*(?:\.[0-9]+)) \s* ExtendFont''')

        lines = (line.strip()
                 for line in file
                 if not empty_re.match(line))
        for line in lines:
            effects, encoding, filename = b'', None, None
            words = word_re.finditer(line)

            # The named groups are mutually exclusive and are
            # referenced below at an estimated order of probability of
            # occurrence based on looking at my copy of pdftex.map.
            # The font names are probably unquoted:
            w = next(words)
            texname = w.group('eff2') or w.group('eff1')
            w = next(words)
            psname = w.group('eff2') or w.group('eff1')

            for w in words:
                # Any effects are almost always quoted:
                eff = w.group('eff1') or w.group('eff2')
                if eff:
                    effects = eff
                    continue
                # Encoding files usually have the .enc suffix
                # and almost never need quoting:
                enc = (w.group('enc4') or w.group('enc3') or
                       w.group('enc2') or w.group('enc1'))
                if enc:
                    if encoding is not None:
                        _log.debug('Multiple encodings for %s = %s',
                                   texname, psname)
                    encoding = enc
                    continue
                # File names are probably unquoted:
                filename = w.group('file2') or w.group('file1')

            effects_dict = {}
            for match in effects_re.finditer(effects):
                slant = match.group('slant')
                if slant:
                    effects_dict['slant'] = float(slant)
                else:
                    effects_dict['extend'] = float(match.group('extend'))

            self._font[texname] = PsFont(
                texname=texname, psname=psname, effects=effects_dict,
                encoding=encoding, filename=filename)
