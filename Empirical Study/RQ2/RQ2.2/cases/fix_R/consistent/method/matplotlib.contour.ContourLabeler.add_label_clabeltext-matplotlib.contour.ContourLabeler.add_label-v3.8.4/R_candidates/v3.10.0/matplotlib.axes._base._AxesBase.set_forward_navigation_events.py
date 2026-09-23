    def set_forward_navigation_events(self, forward):
        """
        Set how pan/zoom events are forwarded to Axes below this one.

        Parameters
        ----------
        forward : bool or "auto"
            Possible values:

            - True: Forward events to other axes with lower or equal zorder.
            - False: Events are only executed on this axes.
            - "auto": Default behaviour (*True* for axes with an invisible
              patch and *False* otherwise)

        See Also
        --------
        matplotlib.axes.Axes.set_navigate

        """
        self._forward_navigation_events = forward
