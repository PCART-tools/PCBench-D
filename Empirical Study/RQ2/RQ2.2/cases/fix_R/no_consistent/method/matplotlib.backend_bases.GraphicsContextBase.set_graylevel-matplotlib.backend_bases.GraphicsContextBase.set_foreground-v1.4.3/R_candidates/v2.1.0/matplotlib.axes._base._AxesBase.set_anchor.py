    def set_anchor(self, anchor):
        """
        *anchor*

          =====  ============
          value  description
          =====  ============
          'C'    Center
          'SW'   bottom left
          'S'    bottom
          'SE'   bottom right
          'E'    right
          'NE'   top right
          'N'    top
          'NW'   top left
          'W'    left
          =====  ============

        """
        if anchor in mtransforms.Bbox.coefs or len(anchor) == 2:
            self._anchor = anchor
        else:
            raise ValueError('argument must be among %s' %
                             ', '.join(mtransforms.Bbox.coefs))
        self.stale = True
