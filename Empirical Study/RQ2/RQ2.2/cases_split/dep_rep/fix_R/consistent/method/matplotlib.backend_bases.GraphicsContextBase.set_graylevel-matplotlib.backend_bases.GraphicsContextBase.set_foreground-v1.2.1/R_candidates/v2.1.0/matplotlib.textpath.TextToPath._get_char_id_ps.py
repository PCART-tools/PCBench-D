    def _get_char_id_ps(self, font, ccode):
        """
        Return a unique id for the given font and character-code set (for tex).
        """
        ps_name = font.get_ps_font_info()[2]
        char_id = urllib_quote('%s-%d' % (ps_name, ccode))
        return char_id
