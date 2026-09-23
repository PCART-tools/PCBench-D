    @_register_style(_style_list, name="-")
    class Curve(_Curve):
        """A simple curve without any arrow head."""

        def __init__(self):  # hide head_length, head_width
            # These attributes (whose values come from backcompat) only matter
            # if someone modifies beginarrow/etc. on an ArrowStyle instance.
            super().__init__(head_length=.2, head_width=.1)
