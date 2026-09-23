    def get_xticklabels(self, minor=False, which=None):
        """
        Get the x tick labels as a list of `~matplotlib.text.Text` instances.

        Parameters
        ----------
        minor : bool, optional
           If True return the minor ticklabels,
           else return the major ticklabels.

        which : None, ('minor', 'major', 'both')
           Overrides *minor*.

           Selects which ticklabels to return

        Returns
        -------
        ret : list
           List of `~matplotlib.text.Text` instances.
        """
        return self.xaxis.get_ticklabels(minor=minor, which=which)
