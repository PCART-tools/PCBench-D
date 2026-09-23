    def __init__(self, shorthand_name=None):
        """
        Creates a new :class:`TransformNode`.

        **shorthand_name** - a string representing the "name" of this
                             transform. The name carries no significance
                             other than to improve the readability of
                             ``str(transform)`` when DEBUG=True.
        """
        self._parents = {}

        # TransformNodes start out as invalid until their values are
        # computed for the first time.
        self._invalid = 1
        self._shorthand_name = shorthand_name or ''
