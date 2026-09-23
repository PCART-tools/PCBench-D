    def _get_char_id(self, font, ccode):
        """
        Return a unique id for the given font and character-code set.
        """
        return urllib.parse.quote('{}-{}'.format(font.postscript_name, ccode))
