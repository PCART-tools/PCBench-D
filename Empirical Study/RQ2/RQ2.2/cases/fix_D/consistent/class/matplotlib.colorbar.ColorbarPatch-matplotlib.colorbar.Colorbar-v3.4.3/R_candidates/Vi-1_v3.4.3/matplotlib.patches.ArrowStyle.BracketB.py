    @_register_style(_style_list, name="-[")
    class BracketB(_Bracket):
        """An arrow with an outward square bracket at its end."""

        def __init__(self, widthB=1., lengthB=0.2, angleB=None):
            """
            Parameters
            ----------
            widthB : float, default: 1.0
                Width of the bracket.

            lengthB : float, default: 0.2
                Length of the bracket.

            angleB : float, default: None
                Angle, in degrees, between the bracket and the line. Zero is
                perpendicular to the line, and positive measures
                counterclockwise.
            """
            super().__init__(None, True,
                             widthB=widthB, lengthB=lengthB, angleB=angleB)
