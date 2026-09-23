    @_register_style(_style_list, name="]-[")
    class BracketAB(_Curve):
        """An arrow with outward square brackets at both ends."""
        arrow = "]-["

        def __init__(self,
                     widthA=1., lengthA=0.2, angleA=0,
                     widthB=1., lengthB=0.2, angleB=0):
            """
            Parameters
            ----------
            widthA, widthB : float, default: 1.0
                Width of the bracket.
            lengthA, lengthB : float, default: 0.2
                Length of the bracket.
            angleA, angleB : float, default: 0 degrees
                Orientation of the bracket, as a counterclockwise angle.
                0 degrees means perpendicular to the line.
            """
            super().__init__(widthA=widthA, lengthA=lengthA, angleA=angleA,
                             widthB=widthB, lengthB=lengthB, angleB=angleB)
