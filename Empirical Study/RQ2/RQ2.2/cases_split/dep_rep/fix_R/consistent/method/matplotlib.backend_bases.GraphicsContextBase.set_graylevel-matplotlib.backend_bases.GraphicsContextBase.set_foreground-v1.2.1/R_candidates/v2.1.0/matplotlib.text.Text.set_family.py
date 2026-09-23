    def set_family(self, fontname):
        """
        Set the font family.  May be either a single string, or a list
        of strings in decreasing priority.  Each string may be either
        a real font name or a generic font class name.  If the latter,
        the specific font names will be looked up in the
        :file:`matplotlibrc` file.

        ACCEPTS: [FONTNAME | 'serif' | 'sans-serif' | 'cursive' | 'fantasy' |
                  'monospace' ]
        """
        self._fontproperties.set_family(fontname)
        self.stale = True
