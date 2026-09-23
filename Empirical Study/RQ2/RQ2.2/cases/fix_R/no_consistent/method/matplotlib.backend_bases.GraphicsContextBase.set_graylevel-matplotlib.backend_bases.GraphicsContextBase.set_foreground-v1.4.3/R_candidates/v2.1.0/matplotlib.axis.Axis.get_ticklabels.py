    def get_ticklabels(self, minor=False, which=None):
        """
        Get the x tick labels as a list of :class:`~matplotlib.text.Text`
        instances.

        Parameters
        ----------
        minor : bool
           If True return the minor ticklabels,
           else return the major ticklabels

        which : None, ('minor', 'major', 'both')
           Overrides `minor`.

           Selects which ticklabels to return

        Returns
        -------
        ret : list
           List of :class:`~matplotlib.text.Text` instances.
        """

        if which is not None:
            if which == 'minor':
                return self.get_minorticklabels()
            elif which == 'major':
                return self.get_majorticklabels()
            elif which == 'both':
                return self.get_majorticklabels() + self.get_minorticklabels()
            else:
                raise ValueError("`which` must be one of ('minor', 'major', "
                                 "'both') not " + str(which))
        if minor:
            return self.get_minorticklabels()
        return self.get_majorticklabels()
