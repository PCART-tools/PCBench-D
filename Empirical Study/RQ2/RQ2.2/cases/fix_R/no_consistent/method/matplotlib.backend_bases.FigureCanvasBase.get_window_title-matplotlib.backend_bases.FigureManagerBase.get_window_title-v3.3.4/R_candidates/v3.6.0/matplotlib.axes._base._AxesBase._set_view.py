    def _set_view(self, view):
        """
        Apply a previously saved view.

        Called when restoring a view, such as with the navigation buttons.

        .. note::

            Intended to be overridden by new projection types, but if not, the
            default implementation restores the view limits. You *must*
            implement :meth:`_get_view` if you implement this method.
        """
        xmin, xmax, ymin, ymax = view
        self.set_xlim((xmin, xmax))
        self.set_ylim((ymin, ymax))
