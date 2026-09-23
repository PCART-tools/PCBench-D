    @docstring.dedent_interpd
    def gca(self, **kwargs):
        """
        Get the current Axes, creating one if necessary.

        The following kwargs are supported for ensuring the returned Axes
        adheres to the given projection etc., and for Axes creation if
        the active Axes does not exist:

        %(Axes_kwdoc)s

        """
        if kwargs:
            _api.warn_deprecated(
                "3.4",
                message="Calling gca() with keyword arguments was deprecated "
                "in Matplotlib %(since)s. Starting %(removal)s, gca() will "
                "take no keyword arguments. The gca() function should only be "
                "used to get the current axes, or if no axes exist, create "
                "new axes with default keyword arguments. To create a new "
                "axes with non-default arguments, use plt.axes() or "
                "plt.subplot().")
        if self._axstack.empty():
            return self.add_subplot(1, 1, 1, **kwargs)
        else:
            return self._axstack()
