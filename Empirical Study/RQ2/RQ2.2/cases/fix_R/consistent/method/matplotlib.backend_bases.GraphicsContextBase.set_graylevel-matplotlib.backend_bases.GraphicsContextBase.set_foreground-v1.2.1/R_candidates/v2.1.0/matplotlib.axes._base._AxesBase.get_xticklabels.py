    def get_xticklabels(self, minor=False, which=None):
        """
        Get the x tick labels as a list of :class:`~matplotlib.text.Text`
        instances.

        Parameters
        ----------
        minor : bool, optional
           If True return the minor ticklabels,
           else return the major ticklabels.

        which : None, ('minor', 'major', 'both')
           Overrides `minor`.

           Selects which ticklabels to return

        Returns
        -------
        ret : list
           List of :class:`~matplotlib.text.Text` instances.
        """
        return cbook.silent_list('Text xticklabel',
                                 self.xaxis.get_ticklabels(minor=minor,
                                                           which=which))
