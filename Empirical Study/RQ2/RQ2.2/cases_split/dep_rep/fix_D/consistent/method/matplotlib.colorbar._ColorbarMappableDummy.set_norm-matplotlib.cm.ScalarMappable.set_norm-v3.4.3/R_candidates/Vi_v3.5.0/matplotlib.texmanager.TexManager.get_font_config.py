    def get_font_config(self):
        ff = rcParams['font.family']
        ff_val = ff[0].lower() if len(ff) == 1 else None
        reduced_notation = False
        if len(ff) == 1 and ff_val in self._font_families:
            self._font_family = ff_val
        elif len(ff) == 1 and ff_val in self._font_info:
            reduced_notation = True
            self._font_family = self._font_types[ff_val]
        else:
            _log.info('font.family must be one of (%s) when text.usetex is '
                      'True. serif will be used by default.',
                      ', '.join(self._font_families))
            self._font_family = 'serif'

        fontconfig = [self._font_family]
        fonts = {}
        for font_family in self._font_families:
            if reduced_notation and self._font_family == font_family:
                fonts[font_family] = self._font_info[ff_val]
            else:
                for font in rcParams['font.' + font_family]:
                    if font.lower() in self._font_info:
                        fonts[font_family] = self._font_info[font.lower()]
                        _log.debug(
                            'family: %s, font: %s, info: %s',
                            font_family, font, self._font_info[font.lower()])
                        break
                    else:
                        _log.debug('%s font is not compatible with usetex.',
                                   font)
                else:
                    _log.info('No LaTeX-compatible font found for the %s font'
                              'family in rcParams. Using default.',
                              font_family)
                    fonts[font_family] = self._font_info[font_family]
            fontconfig.append(fonts[font_family][0])
        # Add a hash of the latex preamble to fontconfig so that the
        # correct png is selected for strings rendered with same font and dpi
        # even if the latex preamble changes within the session
        preamble_bytes = self.get_custom_preamble().encode('utf-8')
        fontconfig.append(hashlib.md5(preamble_bytes).hexdigest())

        # The following packages and commands need to be included in the latex
        # file's preamble:
        cmd = {fonts[family][1]
               for family in ['serif', 'sans-serif', 'monospace']}
        if self._font_family == 'cursive':
            cmd.add(fonts['cursive'][1])
        cmd.add(r'\usepackage{type1cm}')
        self._font_preamble = '\n'.join(sorted(cmd))

        return ''.join(fontconfig)
