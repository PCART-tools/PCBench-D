    @docstring.dedent_interpd
    def gca(self, **kwargs):
        """
        Get the current Axes.

        If there is currently no Axes on this Figure, a new one is created
        using `.Figure.add_subplot`.  (To test whether there is currently an
        Axes on a Figure, check whether ``figure.axes`` is empty.  To test
        whether there is currently a Figure on the pyplot figure stack, check
        whether `.pyplot.get_fignums()` is empty.)

        The following kwargs are supported for ensuring the returned Axes
        adheres to the given projection etc., and for Axes creation if
        the active Axes does not exist:

        %(Axes:kwdoc)s
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
