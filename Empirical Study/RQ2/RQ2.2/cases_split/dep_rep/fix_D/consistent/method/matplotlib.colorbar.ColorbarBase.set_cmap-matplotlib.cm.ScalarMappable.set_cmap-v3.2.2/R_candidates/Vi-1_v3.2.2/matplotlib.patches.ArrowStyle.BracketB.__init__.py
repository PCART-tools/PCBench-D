        def __init__(self, widthB=1., lengthB=0.2, angleB=None):
            """
            Parameters
            ----------
            widthB : float, optional, default : 1.0
                Width of the bracket

            lengthB : float, optional, default : 0.2
                Length of the bracket

            angleB : float, optional, default : None
                Angle between the bracket and the line
            """
            super().__init__(None, True,
                             widthB=widthB, lengthB=lengthB, angleB=angleB)
