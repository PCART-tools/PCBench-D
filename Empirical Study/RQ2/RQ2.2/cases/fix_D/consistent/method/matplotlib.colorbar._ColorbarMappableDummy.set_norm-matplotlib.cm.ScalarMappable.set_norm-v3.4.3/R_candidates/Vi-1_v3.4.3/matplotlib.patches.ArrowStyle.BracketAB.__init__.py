        def __init__(self,
                     widthA=1., lengthA=0.2, angleA=None,
                     widthB=1., lengthB=0.2, angleB=None):
            """
            Parameters
            ----------
            widthA : float, default: 1.0
                Width of the bracket.

            lengthA : float, default: 0.2
                Length of the bracket.

            angleA : float, default: None
                Angle, in degrees, between the bracket and the line. Zero is
                perpendicular to the line, and positive measures
                counterclockwise.

            widthB : float, default: 1.0
                Width of the bracket.

            lengthB : float, default: 0.2
                Length of the bracket.

            angleB : float, default: None
                Angle, in degrees, between the bracket and the line. Zero is
                perpendicular to the line, and positive measures
                counterclockwise.
            """
            super().__init__(True, True,
                             widthA=widthA, lengthA=lengthA, angleA=angleA,
                             widthB=widthB, lengthB=lengthB, angleB=angleB)
