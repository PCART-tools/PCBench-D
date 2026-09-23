        def __init__(self,
                     widthA=1., angleA=None,
                     widthB=1., angleB=None):
            """
            Parameters
            ----------
            widthA : float, optional, default : 1.0
                Width of the bracket

            angleA : float, optional, default : None
                Angle between the bracket and the line

            widthB : float, optional, default : 1.0
                Width of the bracket

            angleB : float, optional, default : None
                Angle between the bracket and the line
            """

            super(ArrowStyle.BarAB, self).__init__(
                        True, True, widthA=widthA, lengthA=0, angleA=angleA,
                        widthB=widthB, lengthB=0, angleB=angleB)
