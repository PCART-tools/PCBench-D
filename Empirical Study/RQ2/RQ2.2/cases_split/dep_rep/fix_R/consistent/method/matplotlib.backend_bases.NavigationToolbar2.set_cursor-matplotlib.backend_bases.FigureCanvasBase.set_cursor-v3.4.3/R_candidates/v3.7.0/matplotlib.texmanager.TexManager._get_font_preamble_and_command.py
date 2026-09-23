    @classmethod
    def _get_font_preamble_and_command(cls):
        requested_family, is_reduced_font = cls._get_font_family_and_reduced()

        preambles = {}
        for font_family in cls._font_families:
            if is_reduced_font and font_family == requested_family:
                preambles[font_family] = cls._font_preambles[
                    mpl.rcParams['font.family'][0].lower()]
            else:
                for font in mpl.rcParams['font.' + font_family]:
                    if font.lower() in cls._font_preambles:
                        preambles[font_family] = \
                            cls._font_preambles[font.lower()]
                        _log.debug(
                            'family: %s, font: %s, info: %s',
                            font_family, font,
                            cls._font_preambles[font.lower()])
                        break
                    else:
                        _log.debug('%s font is not compatible with usetex.',
                                   font)
                else:
                    _log.info('No LaTeX-compatible font found for the %s font'
                              'family in rcParams. Using default.',
                              font_family)
                    preambles[font_family] = cls._font_preambles[font_family]

        # The following packages and commands need to be included in the latex
        # file's preamble:
        cmd = {preambles[family]
               for family in ['serif', 'sans-serif', 'monospace']}
        if requested_family == 'cursive':
            cmd.add(preambles['cursive'])
        cmd.add(r'\usepackage{type1cm}')
        preamble = '\n'.join(sorted(cmd))
        fontcmd = (r'\sffamily' if requested_family == 'sans-serif' else
                   r'\ttfamily' if requested_family == 'monospace' else
                   r'\rmfamily')
        return preamble, fontcmd
