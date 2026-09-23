    def select(self, crit, axis=0):
        """
        Return data corresponding to axis labels matching criteria.

        .. deprecated:: 0.21.0
            Use df.loc[df.index.map(crit)] to select via labels

        Parameters
        ----------
        crit : function
            To be called on each index (label). Should return True or False
        axis : int

        Returns
        -------
        selection : same type as caller
        """
        warnings.warn("'select' is deprecated and will be removed in a "
                      "future release. You can use "
                      ".loc[labels.map(crit)] as a replacement",
                      FutureWarning, stacklevel=2)

        axis = self._get_axis_number(axis)
        axis_name = self._get_axis_name(axis)
        axis_values = self._get_axis(axis)

        if len(axis_values) > 0:
            new_axis = axis_values[
                np.asarray([bool(crit(label)) for label in axis_values])]
        else:
            new_axis = axis_values

        return self.reindex(**{axis_name: new_axis})
