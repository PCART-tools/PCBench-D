    @_register_style(_style_list, name="->")
    class CurveB(_Curve):
        """An arrow with a head at its end point."""

        def __init__(self, head_length=.4, head_width=.2):
            """
            Parameters
            ----------
            head_length : float, default: 0.4
                Length of the arrow head.

            head_width : float, default: 0.2
                Width of the arrow head.
            """
            super().__init__(beginarrow=False, endarrow=True,
                             head_length=head_length, head_width=head_width)
