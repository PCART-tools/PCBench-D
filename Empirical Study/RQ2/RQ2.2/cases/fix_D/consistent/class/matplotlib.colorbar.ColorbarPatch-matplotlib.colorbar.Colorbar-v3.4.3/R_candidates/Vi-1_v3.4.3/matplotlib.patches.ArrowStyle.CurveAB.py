    @_register_style(_style_list, name="<->")
    class CurveAB(_Curve):
        """An arrow with heads both at the begin and the end point."""

        def __init__(self, head_length=.4, head_width=.2):
            """
            Parameters
            ----------
            head_length : float, default: 0.4
                Length of the arrow head.

            head_width : float, default: 0.2
                Width of the arrow head.
            """
            super().__init__(beginarrow=True, endarrow=True,
                             head_length=head_length, head_width=head_width)
