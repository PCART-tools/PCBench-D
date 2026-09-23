    def get_yticklabels(self, minor=False, which=None):
        """
        Get the y tick labels as a list of :class:`~matplotlib.text.Text`
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
        return cbook.silent_list('Text yticklabel',
                                 self.yaxis.get_ticklabels(minor=minor,
                                                           which=which))
