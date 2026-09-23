    def _get_view(self):
        """
        Save information required to reproduce the current view.

        This method is called before a view is changed, such as during a pan or zoom
        initiated by the user.  It returns an opaque object that describes the current
        view, in a format compatible with :meth:`_set_view`.

        The default implementation saves the view limits and autoscaling state.
        Subclasses may override this as needed, as long as :meth:`_set_view` is also
        adjusted accordingly.
        """
        return {
            "xlim": self.get_xlim(), "autoscalex_on": self.get_autoscalex_on(),
            "ylim": self.get_ylim(), "autoscaley_on": self.get_autoscaley_on(),
        }
