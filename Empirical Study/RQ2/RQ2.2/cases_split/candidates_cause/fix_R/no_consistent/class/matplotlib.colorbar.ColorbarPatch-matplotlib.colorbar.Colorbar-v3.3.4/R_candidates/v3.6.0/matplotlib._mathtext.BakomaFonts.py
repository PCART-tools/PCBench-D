class BakomaFonts(TruetypeFonts):
    """
    Use the Bakoma TrueType fonts for rendering.

    Symbols are strewn about a number of font files, each of which has
    its own proprietary 8-bit encoding.
    """
    _fontmap = {
        'cal': 'cmsy10',
        'rm':  'cmr10',
        'tt':  'cmtt10',
        'it':  'cmmi10',
        'bf':  'cmb10',
        'sf':  'cmss10',
        'ex':  'cmex10',
    }

    def __init__(self, *args, **kwargs):
        self._stix_fallback = StixFonts(*args, **kwargs)

        super().__init__(*args, **kwargs)
        self.fontmap = {}
        for key, val in self._fontmap.items():
            fullpath = findfont(val)
            self.fontmap[key] = fullpath
            self.fontmap[val] = fullpath

    _slanted_symbols = set(r"\int \oint".split())

    def _get_glyph(self, fontname, font_class, sym):
        font = None
        if fontname in self.fontmap and sym in latex_to_bakoma:
            basename, num = latex_to_bakoma[sym]
            slanted = (basename == "cmmi10") or sym in self._slanted_symbols
            font = self._get_font(basename)
        elif len(sym) == 1:
            slanted = (fontname == "it")
            font = self._get_font(fontname)
            if font is not None:
                num = ord(sym)
        if font is not None and font.get_char_index(num) != 0:
            return font, num, slanted
        else:
            return self._stix_fallback._get_glyph(fontname, font_class, sym)

    # The Bakoma fonts contain many pre-sized alternatives for the
    # delimiters.  The AutoSizedChar class will use these alternatives
    # and select the best (closest sized) glyph.
    _size_alternatives = {
        '(':           [('rm', '('), ('ex', '\xa1'), ('ex', '\xb3'),
                        ('ex', '\xb5'), ('ex', '\xc3')],
        ')':           [('rm', ')'), ('ex', '\xa2'), ('ex', '\xb4'),
                        ('ex', '\xb6'), ('ex', '\x21')],
        '{':           [('cal', '{'), ('ex', '\xa9'), ('ex', '\x6e'),
                        ('ex', '\xbd'), ('ex', '\x28')],
        '}':           [('cal', '}'), ('ex', '\xaa'), ('ex', '\x6f'),
                        ('ex', '\xbe'), ('ex', '\x29')],
        # The fourth size of '[' is mysteriously missing from the BaKoMa
        # font, so I've omitted it for both '[' and ']'
        '[':           [('rm', '['), ('ex', '\xa3'), ('ex', '\x68'),
                        ('ex', '\x22')],
        ']':           [('rm', ']'), ('ex', '\xa4'), ('ex', '\x69'),
                        ('ex', '\x23')],
        r'\lfloor':    [('ex', '\xa5'), ('ex', '\x6a'),
                        ('ex', '\xb9'), ('ex', '\x24')],
        r'\rfloor':    [('ex', '\xa6'), ('ex', '\x6b'),
                        ('ex', '\xba'), ('ex', '\x25')],
        r'\lceil':     [('ex', '\xa7'), ('ex', '\x6c'),
                        ('ex', '\xbb'), ('ex', '\x26')],
        r'\rceil':     [('ex', '\xa8'), ('ex', '\x6d'),
                        ('ex', '\xbc'), ('ex', '\x27')],
        r'\langle':    [('ex', '\xad'), ('ex', '\x44'),
                        ('ex', '\xbf'), ('ex', '\x2a')],
        r'\rangle':    [('ex', '\xae'), ('ex', '\x45'),
                        ('ex', '\xc0'), ('ex', '\x2b')],
        r'\__sqrt__':  [('ex', '\x70'), ('ex', '\x71'),
                        ('ex', '\x72'), ('ex', '\x73')],
        r'\backslash': [('ex', '\xb2'), ('ex', '\x2f'),
                        ('ex', '\xc2'), ('ex', '\x2d')],
        r'/':          [('rm', '/'), ('ex', '\xb1'), ('ex', '\x2e'),
                        ('ex', '\xcb'), ('ex', '\x2c')],
        r'\widehat':   [('rm', '\x5e'), ('ex', '\x62'), ('ex', '\x63'),
                        ('ex', '\x64')],
        r'\widetilde': [('rm', '\x7e'), ('ex', '\x65'), ('ex', '\x66'),
                        ('ex', '\x67')],
        r'<':          [('cal', 'h'), ('ex', 'D')],
        r'>':          [('cal', 'i'), ('ex', 'E')]
        }

    for alias, target in [(r'\leftparen', '('),
                          (r'\rightparent', ')'),
                          (r'\leftbrace', '{'),
                          (r'\rightbrace', '}'),
                          (r'\leftbracket', '['),
                          (r'\rightbracket', ']'),
                          (r'\{', '{'),
                          (r'\}', '}'),
                          (r'\[', '['),
                          (r'\]', ']')]:
        _size_alternatives[alias] = _size_alternatives[target]

    def get_sized_alternatives_for_symbol(self, fontname, sym):
        return self._size_alternatives.get(sym, [(fontname, sym)])
