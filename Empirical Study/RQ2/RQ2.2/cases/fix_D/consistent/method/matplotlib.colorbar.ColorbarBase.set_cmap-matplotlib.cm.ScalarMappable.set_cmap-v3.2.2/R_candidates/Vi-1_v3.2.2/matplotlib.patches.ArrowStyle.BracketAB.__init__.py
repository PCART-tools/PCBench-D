        def __init__(self,
                     widthA=1., lengthA=0.2, angleA=None,
                     widthB=1., lengthB=0.2, angleB=None):
            """
            Parameters
            ----------
            widthA : float, optional, default : 1.0
                Width of the bracket

            lengthA : float, optional, default : 0.2
                Length of the bracket

            angleA : float, optional, default : None
                Angle between the bracket and the line

            widthB : float, optional, default : 1.0
                Width of the bracket

            lengthB : float, optional, default : 0.2
                Length of the bracket

            angleB : float, optional, default : None
                Angle between the bracket and the line
            """
            super().__init__(True, True,
                             widthA=widthA, lengthA=lengthA, angleA=angleA,
                             widthB=widthB, lengthB=lengthB, angleB=angleB)
