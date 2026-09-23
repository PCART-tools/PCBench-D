    def get_ticks_direction(self, minor=False):
        """
        Get the tick directions as a numpy array

        Parameters
        ----------
        minor : boolean
            True to return the minor tick directions,
            False to return the major tick directions,
            Default is False

        Returns
        -------
        numpy array of tick directions
        """
        if minor:
            return np.array(
                [tick._tickdir for tick in self.get_minor_ticks()])
        else:
            return np.array(
                [tick._tickdir for tick in self.get_major_ticks()])
