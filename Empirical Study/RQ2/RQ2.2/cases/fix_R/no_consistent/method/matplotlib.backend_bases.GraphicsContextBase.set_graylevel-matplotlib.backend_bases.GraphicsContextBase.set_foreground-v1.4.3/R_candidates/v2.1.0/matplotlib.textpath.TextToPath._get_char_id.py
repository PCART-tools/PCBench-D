    def _get_char_id(self, font, ccode):
        """
        Return a unique id for the given font and character-code set.
        """
        sfnt = font.get_sfnt()
        try:
            ps_name = sfnt[(1, 0, 0, 6)].decode('macroman')
        except KeyError:
            ps_name = sfnt[(3, 1, 0x0409, 6)].decode('utf-16be')
        char_id = urllib_quote('%s-%x' % (ps_name, ccode))
        return char_id
