        def __init__(self,
                     widthA=1., angleA=None,
                     widthB=1., angleB=None):
            """
            Parameters
            ----------
            widthA : float, default: 1.0
                Width of the bracket.

            angleA : float, default: None
                Angle, in degrees, between the bracket and the line. Zero is
                perpendicular to the line, and positive measures
                counterclockwise.

            widthB : float, default: 1.0
                Width of the bracket.

            angleB : float, default: None
                Angle, in degrees, between the bracket and the line. Zero is
                perpendicular to the line, and positive measures
                counterclockwise.
            """
            super().__init__(True, True,
                             widthA=widthA, lengthA=0, angleA=angleA,
                             widthB=widthB, lengthB=0, angleB=angleB)
