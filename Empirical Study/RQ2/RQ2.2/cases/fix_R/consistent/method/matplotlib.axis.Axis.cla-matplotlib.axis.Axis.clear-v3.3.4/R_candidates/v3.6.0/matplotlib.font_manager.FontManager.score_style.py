    def score_style(self, style1, style2):
        """
        Return a match score between *style1* and *style2*.

        An exact match returns 0.0.

        A match between 'italic' and 'oblique' returns 0.1.

        No match returns 1.0.
        """
        if style1 == style2:
            return 0.0
        elif (style1 in ('italic', 'oblique')
              and style2 in ('italic', 'oblique')):
            return 0.1
        return 1.0
