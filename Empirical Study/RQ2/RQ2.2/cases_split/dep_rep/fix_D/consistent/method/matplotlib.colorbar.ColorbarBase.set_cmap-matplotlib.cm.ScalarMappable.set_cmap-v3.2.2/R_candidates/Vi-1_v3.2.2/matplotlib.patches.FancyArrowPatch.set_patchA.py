    def set_patchA(self, patchA):
        """
        Set the tail patch.

        Parameters
        ----------
        patchA : Patch
            :class:`matplotlib.patch.Patch` instance.
        """
        self.patchA = patchA
        self.stale = True
