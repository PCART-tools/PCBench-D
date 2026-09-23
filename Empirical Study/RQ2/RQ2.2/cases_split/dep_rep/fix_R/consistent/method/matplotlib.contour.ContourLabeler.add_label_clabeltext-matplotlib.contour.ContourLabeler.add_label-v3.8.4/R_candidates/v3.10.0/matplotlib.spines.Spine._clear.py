    def _clear(self):
        """
        Clear things directly related to the spine.

        In this way it is possible to avoid clearing the Axis as well when calling
        from library code where it is known that the Axis is cleared separately.
        """
        self._position = None  # clear position
