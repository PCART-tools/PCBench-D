    def set_size(self, fontsize):
        """
        Set the font size.  May be either a size string, relative to
        the default font size, or an absolute font size in points.

        ACCEPTS: [size in points | 'xx-small' | 'x-small' | 'small' |
                  'medium' | 'large' | 'x-large' | 'xx-large' ]
        """
        self._fontproperties.set_size(fontsize)
        self.stale = True
