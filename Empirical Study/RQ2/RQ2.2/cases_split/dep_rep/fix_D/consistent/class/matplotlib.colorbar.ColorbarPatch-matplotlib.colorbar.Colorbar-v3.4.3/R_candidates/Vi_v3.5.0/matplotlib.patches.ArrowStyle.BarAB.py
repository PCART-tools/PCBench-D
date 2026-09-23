    @_register_style(_style_list, name="|-|")
    class BarAB(_Curve):
        """An arrow with vertical bars ``|`` at both ends."""
        arrow = "|-|"

        def __init__(self, widthA=1., angleA=0, widthB=1., angleB=0):
            """
            Parameters
            ----------
            widthA, widthB : float, default: 1.0
                Width of the bracket.
            angleA, angleB : float, default: 0 degrees
                Orientation of the bracket, as a counterclockwise angle.
                0 degrees means perpendicular to the line.
            """
            super().__init__(widthA=widthA, lengthA=0, angleA=angleA,
                             widthB=widthB, lengthB=0, angleB=angleB)
