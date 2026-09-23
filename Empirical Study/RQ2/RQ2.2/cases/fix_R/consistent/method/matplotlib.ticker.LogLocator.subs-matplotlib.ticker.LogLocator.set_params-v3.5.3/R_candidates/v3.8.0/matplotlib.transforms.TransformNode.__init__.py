    def __init__(self, shorthand_name=None):
        """
        Parameters
        ----------
        shorthand_name : str
            A string representing the "name" of the transform. The name carries
            no significance other than to improve the readability of
            ``str(transform)`` when DEBUG=True.
        """
        self._parents = {}
        # Initially invalid, until first computation.
        self._invalid = self._INVALID_FULL
        self._shorthand_name = shorthand_name or ''
