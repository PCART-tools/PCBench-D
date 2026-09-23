    def _get_view(self):
        """
        Save information required to reproduce the current view.

        Called before a view is changed, such as during a pan or zoom
        initiated by the user. You may return any information you deem
        necessary to describe the view.

        .. note::

            Intended to be overridden by new projection types, but if not, the
            default implementation saves the view limits. You *must* implement
            :meth:`_set_view` if you implement this method.
        """
        xmin, xmax = self.get_xlim()
        ymin, ymax = self.get_ylim()
        return xmin, xmax, ymin, ymax
