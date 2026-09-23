    def copy(self, deep=True):
        """
        Make deep or shallow copy of BlockManager

        Parameters
        ----------
        deep : boolean, default True
            If False, return shallow copy (do not copy data)

        Returns
        -------
        copy : BlockManager
        """
        if deep:
            new_axes = [ax.view() for ax in self.axes]
        else:
            new_axes = list(self.axes)
        return self.apply('copy', axes=new_axes, deep=deep,
                          do_integrity_check=False)
