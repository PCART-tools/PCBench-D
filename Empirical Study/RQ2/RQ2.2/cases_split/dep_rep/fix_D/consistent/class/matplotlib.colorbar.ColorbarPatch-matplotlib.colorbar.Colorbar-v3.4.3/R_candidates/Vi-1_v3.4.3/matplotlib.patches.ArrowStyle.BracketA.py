    @_register_style(_style_list, name="]-")
    class BracketA(_Bracket):
        """An arrow with an outward square bracket at its start."""

        def __init__(self, widthA=1., lengthA=0.2, angleA=None):
            """
            Parameters
            ----------
            widthA : float, default: 1.0
                Width of the bracket.

            lengthA : float, default: 0.2
                Length of the bracket.

            angleA : float, default: None
                Angle between the bracket and the line.
            """
            super().__init__(True, None,
                             widthA=widthA, lengthA=lengthA, angleA=angleA)
