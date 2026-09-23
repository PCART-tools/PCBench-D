    def copy(self, deep=True):
        """
        Make deep or shallow copy of BlockManager

        Parameters
        ----------
        deep : boolean o rstring, default True
            If False, return shallow copy (do not copy data)
            If 'all', copy data and a deep copy of the index

        Returns
        -------
        copy : BlockManager
        """

        # this preserves the notion of view copying of axes
        if deep:
            if deep == 'all':
                copy = lambda ax: ax.copy(deep=True)
            else:
                copy = lambda ax: ax.view()
            new_axes = [ copy(ax) for ax in self.axes]
        else:
            new_axes = list(self.axes)
        return self.apply('copy', axes=new_axes, deep=deep,
                          do_integrity_check=False)
