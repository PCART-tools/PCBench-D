    def get_snap(self):
        """
        Return the snap setting.

        See `.set_snap` for details.
        """
        if mpl.rcParams['path.snap']:
            return self._snap
        else:
            return False
