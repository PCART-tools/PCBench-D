    def xlat(self, text):
        """ Translate *text*, returns the modified text. """
        return self._make_regex().sub(self, text)
