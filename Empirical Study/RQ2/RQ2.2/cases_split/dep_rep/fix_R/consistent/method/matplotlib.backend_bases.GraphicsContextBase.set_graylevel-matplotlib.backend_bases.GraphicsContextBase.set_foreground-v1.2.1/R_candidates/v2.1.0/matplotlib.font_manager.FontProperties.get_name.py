    def get_name(self):
        """
        Return the name of the font that best matches the font
        properties.
        """
        return get_font(findfont(self)).family_name
