    def get_font_config(self):
        ff = rcParams['font.family']
        if len(ff) == 1 and ff[0].lower() in self.font_families:
            self.font_family = ff[0].lower()
        else:
            _log.info('font.family must be one of (%s) when text.usetex is '
                      'True. serif will be used by default.',
                      ', '.join(self.font_families))
            self.font_family = 'serif'

        fontconfig = [self.font_family]
        for font_family in self.font_families:
            for font in rcParams['font.' + font_family]:
                if font.lower() in self.font_info:
                    self._fonts[font_family] = self.font_info[font.lower()]
                    _log.debug('family: %s, font: %s, info: %s',
                               font_family, font, self.font_info[font.lower()])
                    break
                else:
                    _log.debug('%s font is not compatible with usetex.', font)
            else:
                _log.info('No LaTeX-compatible font found for the %s font '
                          'family in rcParams. Using default.', font_family)
                self._fonts[font_family] = self.font_info[font_family]
            fontconfig.append(self._fonts[font_family][0])
        # Add a hash of the latex preamble to fontconfig so that the
        # correct png is selected for strings rendered with same font and dpi
        # even if the latex preamble changes within the session
        preamble_bytes = self.get_custom_preamble().encode('utf-8')
        fontconfig.append(hashlib.md5(preamble_bytes).hexdigest())

        # The following packages and commands need to be included in the latex
        # file's preamble:
        cmd = [self._fonts['serif'][1],
               self._fonts['sans-serif'][1],
               self._fonts['monospace'][1]]
        if self.font_family == 'cursive':
            cmd.append(self._fonts['cursive'][1])
        self._font_preamble = '\n'.join([r'\usepackage{type1cm}', *cmd])

        return ''.join(fontconfig)
