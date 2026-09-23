    @classmethod
    def get_font_preamble(cls):
        """
        Return a string containing font configuration for the tex preamble.
        """
        font_preamble, command = cls._get_font_preamble_and_command()
        return font_preamble
