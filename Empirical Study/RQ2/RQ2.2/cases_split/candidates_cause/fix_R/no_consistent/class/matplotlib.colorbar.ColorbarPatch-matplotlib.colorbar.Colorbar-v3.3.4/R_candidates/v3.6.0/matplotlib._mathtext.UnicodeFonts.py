class UnicodeFonts(TruetypeFonts):
    """
    An abstract base class for handling Unicode fonts.

    While some reasonably complete Unicode fonts (such as DejaVu) may
    work in some situations, the only Unicode font I'm aware of with a
    complete set of math symbols is STIX.

    This class will "fallback" on the Bakoma fonts when a required
    symbol can not be found in the font.
    """

    def __init__(self, *args, **kwargs):
        # This must come first so the backend's owner is set correctly
        fallback_rc = mpl.rcParams['mathtext.fallback']
        font_cls = {'stix': StixFonts,
                    'stixsans': StixSansFonts,
                    'cm': BakomaFonts
                    }.get(fallback_rc)
        self._fallback_font = font_cls(*args, **kwargs) if font_cls else None

        super().__init__(*args, **kwargs)
        self.fontmap = {}
        for texfont in "cal rm tt it bf sf".split():
            prop = mpl.rcParams['mathtext.' + texfont]
            font = findfont(prop)
            self.fontmap[texfont] = font
        prop = FontProperties('cmex10')
        font = findfont(prop)
        self.fontmap['ex'] = font

        # include STIX sized alternatives for glyphs if fallback is STIX
        if isinstance(self._fallback_font, StixFonts):
            stixsizedaltfonts = {
                 0: 'STIXGeneral',
                 1: 'STIXSizeOneSym',
                 2: 'STIXSizeTwoSym',
                 3: 'STIXSizeThreeSym',
                 4: 'STIXSizeFourSym',
                 5: 'STIXSizeFiveSym'}

            for size, name in stixsizedaltfonts.items():
                fullpath = findfont(name)
                self.fontmap[size] = fullpath
                self.fontmap[name] = fullpath

    _slanted_symbols = set(r"\int \oint".split())

    def _map_virtual_font(self, fontname, font_class, uniindex):
        return fontname, uniindex

    def _get_glyph(self, fontname, font_class, sym):
        try:
            uniindex = get_unicode_index(sym)
            found_symbol = True
        except ValueError:
            uniindex = ord('?')
            found_symbol = False
            _log.warning("No TeX to Unicode mapping for {!a}.".format(sym))

        fontname, uniindex = self._map_virtual_font(
            fontname, font_class, uniindex)

        new_fontname = fontname

        # Only characters in the "Letter" class should be italicized in 'it'
        # mode.  Greek capital letters should be Roman.
        if found_symbol:
            if fontname == 'it' and uniindex < 0x10000:
                char = chr(uniindex)
                if (unicodedata.category(char)[0] != "L"
                        or unicodedata.name(char).startswith("GREEK CAPITAL")):
                    new_fontname = 'rm'

            slanted = (new_fontname == 'it') or sym in self._slanted_symbols
            found_symbol = False
            font = self._get_font(new_fontname)
            if font is not None:
                if font.family_name == "cmr10" and uniindex == 0x2212:
                    # minus sign exists in cmsy10 (not cmr10)
                    font = get_font(
                        cbook._get_data_path("fonts/ttf/cmsy10.ttf"))
                    uniindex = 0xa1
                glyphindex = font.get_char_index(uniindex)
                if glyphindex != 0:
                    found_symbol = True

        if not found_symbol:
            if self._fallback_font:
                if (fontname in ('it', 'regular')
                        and isinstance(self._fallback_font, StixFonts)):
                    fontname = 'rm'

                g = self._fallback_font._get_glyph(fontname, font_class, sym)
                family = g[0].family_name
                if family in list(BakomaFonts._fontmap.values()):
                    family = "Computer Modern"
                _log.info("Substituting symbol %s from %s", sym, family)
                return g

            else:
                if (fontname in ('it', 'regular')
                        and isinstance(self, StixFonts)):
                    return self._get_glyph('rm', font_class, sym)
                _log.warning("Font {!r} does not have a glyph for {!a} "
                             "[U+{:x}], substituting with a dummy "
                             "symbol.".format(new_fontname, sym, uniindex))
                font = self._get_font('rm')
                uniindex = 0xA4  # currency char, for lack of anything better
                slanted = False

        return font, uniindex, slanted

    def get_sized_alternatives_for_symbol(self, fontname, sym):
        if self._fallback_font:
            return self._fallback_font.get_sized_alternatives_for_symbol(
                fontname, sym)
        return [(fontname, sym)]
