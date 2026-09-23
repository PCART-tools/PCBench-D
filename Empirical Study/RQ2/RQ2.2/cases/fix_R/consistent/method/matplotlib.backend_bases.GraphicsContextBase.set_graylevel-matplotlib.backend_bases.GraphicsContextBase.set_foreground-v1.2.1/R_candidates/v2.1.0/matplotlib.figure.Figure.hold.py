    @cbook.deprecated("2.0")
    def hold(self, b=None):
        """
        Set the hold state.  If hold is None (default), toggle the
        hold state.  Else set the hold state to boolean value b.

        e.g.::

            hold()      # toggle hold
            hold(True)  # hold is on
            hold(False) # hold is off

        All "hold" machinery is deprecated.
        """
        if b is None:
            self._hold = not self._hold
        else:
            self._hold = b
