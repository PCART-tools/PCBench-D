    def __init__(self):

        if self.texcache is None:
            raise RuntimeError(
                ('Cannot create TexManager, as there is no cache directory '
                 'available'))

        mkdirs(self.texcache)
        ff = rcParams['font.family']
        if len(ff) == 1 and ff[0].lower() in self.font_families:
            self.font_family = ff[0].lower()
        elif isinstance(ff, six.string_types) and ff.lower() in self.font_families:
            self.font_family = ff.lower()
        else:
            mpl.verbose.report(
                'font.family must be one of (%s) when text.usetex is True. '
                'serif will be used by default.' %
                   ', '.join(self.font_families),
                'helpful')
            self.font_family = 'serif'

        fontconfig = [self.font_family]
        for font_family, font_family_attr in [(ff, ff.replace('-', '_'))
                                              for ff in self.font_families]:
            for font in rcParams['font.' + font_family]:
                if font.lower() in self.font_info:
                    setattr(self, font_family_attr,
                            self.font_info[font.lower()])
                    if DEBUG:
                        print('family: %s, font: %s, info: %s' %
                              (font_family, font,
                               self.font_info[font.lower()]))
                    break
                else:
                    if DEBUG:
                        print('$s font is not compatible with usetex')
            else:
                mpl.verbose.report('No LaTeX-compatible font found for the '
                                   '%s font family in rcParams. Using '
                                   'default.' % font_family, 'helpful')
                setattr(self, font_family_attr, self.font_info[font_family])
            fontconfig.append(getattr(self, font_family_attr)[0])
        # Add a hash of the latex preamble to self._fontconfig so that the
        # correct png is selected for strings rendered with same font and dpi
        # even if the latex preamble changes within the session
        preamble_bytes = six.text_type(self.get_custom_preamble()).encode('utf-8')
        fontconfig.append(md5(preamble_bytes).hexdigest())
        self._fontconfig = ''.join(fontconfig)

        # The following packages and commands need to be included in the latex
        # file's preamble:
        cmd = [self.serif[1], self.sans_serif[1], self.monospace[1]]
        if self.font_family == 'cursive':
            cmd.append(self.cursive[1])
        while '\\usepackage{type1cm}' in cmd:
            cmd.remove('\\usepackage{type1cm}')
        cmd = '\n'.join(cmd)
        self._font_preamble = '\n'.join(['\\usepackage{type1cm}', cmd,
                                         '\\usepackage{textcomp}'])
