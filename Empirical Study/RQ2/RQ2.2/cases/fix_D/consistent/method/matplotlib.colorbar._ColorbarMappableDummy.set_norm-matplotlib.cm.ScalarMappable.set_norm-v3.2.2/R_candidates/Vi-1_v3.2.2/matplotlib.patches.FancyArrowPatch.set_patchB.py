    def set_patchB(self, patchB):
        """
        Set the head patch.

        Parameters
        ----------
        patchB : Patch
            :class:`matplotlib.patch.Patch` instance.
        """
        self.patchB = patchB
        self.stale = True
