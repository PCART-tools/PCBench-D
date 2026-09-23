        def __init__(self, widthB=1., lengthB=0.2, angleB=None):
            """
            Parameters
            ----------
            widthB : float, default: 1.0
                Width of the bracket.

            lengthB : float, default: 0.2
                Length of the bracket.

            angleB : float, default: None
                Angle between the bracket and the line.
            """
            super().__init__(None, True,
                             widthB=widthB, lengthB=lengthB, angleB=angleB)
