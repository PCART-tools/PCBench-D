    def _map_virtual_font(self, fontname: str, font_class: str,
                          uniindex: int) -> tuple[str, int]:
        # Handle these "fonts" that are actually embedded in
        # other fonts.
        font_mapping = stix_virtual_fonts.get(fontname)
        if (self._sans and font_mapping is None
                and fontname not in ('regular', 'default')):
            font_mapping = stix_virtual_fonts['sf']
            doing_sans_conversion = True
        else:
            doing_sans_conversion = False

        if isinstance(font_mapping, dict):
            try:
                mapping = font_mapping[font_class]
            except KeyError:
                mapping = font_mapping['rm']
        elif isinstance(font_mapping, list):
            mapping = font_mapping
        else:
            mapping = None

        if mapping is not None:
            # Binary search for the source glyph
            lo = 0
            hi = len(mapping)
            while lo < hi:
                mid = (lo+hi)//2
                range = mapping[mid]
                if uniindex < range[0]:
                    hi = mid
                elif uniindex <= range[1]:
                    break
                else:
                    lo = mid + 1

            if range[0] <= uniindex <= range[1]:
                uniindex = uniindex - range[0] + range[3]
                fontname = range[2]
            elif not doing_sans_conversion:
                # This will generate a dummy character
                uniindex = 0x1
                fontname = mpl.rcParams['mathtext.default']

        # Fix some incorrect glyphs.
        if fontname in ('rm', 'it'):
            uniindex = stix_glyph_fixes.get(uniindex, uniindex)

        # Handle private use area glyphs
        if fontname in ('it', 'rm', 'bf', 'bfit') and 0xe000 <= uniindex <= 0xf8ff:
            fontname = 'nonuni' + fontname

        return fontname, uniindex
