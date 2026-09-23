    def get_snap(self):
        """
        Returns the snap setting.

        See `.set_snap` for details.
        """
        if rcParams['path.snap']:
            return self._snap
        else:
            return False
