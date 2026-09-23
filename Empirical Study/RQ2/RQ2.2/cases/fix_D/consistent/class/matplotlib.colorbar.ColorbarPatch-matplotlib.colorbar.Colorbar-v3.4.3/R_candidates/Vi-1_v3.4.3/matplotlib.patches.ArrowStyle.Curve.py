    @_register_style(_style_list, name="-")
    class Curve(_Curve):
        """A simple curve without any arrow head."""

        def __init__(self):
            super().__init__(beginarrow=False, endarrow=False)
