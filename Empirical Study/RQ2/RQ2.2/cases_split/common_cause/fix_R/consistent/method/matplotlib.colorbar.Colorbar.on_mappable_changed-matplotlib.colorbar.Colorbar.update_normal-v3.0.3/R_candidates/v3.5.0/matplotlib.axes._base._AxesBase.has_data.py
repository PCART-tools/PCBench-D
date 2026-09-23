    def has_data(self):
        """
        Return whether any artists have been added to the Axes.

        This should not be used to determine whether the *dataLim*
        need to be updated, and may not actually be useful for
        anything.
        """
        return any(isinstance(a, (mcoll.Collection, mimage.AxesImage,
                                  mlines.Line2D, mpatches.Patch))
                   for a in self._children)
