    def get_name_char(self, c, isord=False):
        """
        Get the name of the character, i.e., ';' is 'semicolon'
        """
        if not isord:
            c = ord(c)
        wx, name, bbox = self._metrics[c]
        return name
