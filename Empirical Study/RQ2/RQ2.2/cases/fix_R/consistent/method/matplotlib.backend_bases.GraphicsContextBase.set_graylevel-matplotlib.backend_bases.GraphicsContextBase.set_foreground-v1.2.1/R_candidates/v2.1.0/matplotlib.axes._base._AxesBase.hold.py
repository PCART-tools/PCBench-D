    @cbook.deprecated("2.0", message=_hold_msg)
    def hold(self, b=None):
        """
        Set the hold state

        The ``hold`` mechanism is deprecated and will be removed in
        v3.0.  The behavior will remain consistent with the
        long-time default value of True.

        If *hold* is *None* (default), toggle the *hold* state.  Else
        set the *hold* state to boolean value *b*.

        Examples::

          # toggle hold
          hold()

          # turn hold on
          hold(True)

          # turn hold off
          hold(False)

        When hold is *True*, subsequent plot commands will be added to
        the current axes.  When hold is *False*, the current axes and
        figure will be cleared on the next plot command

        """
        if b is None:
            self._hold = not self._hold
        else:
            self._hold = b
