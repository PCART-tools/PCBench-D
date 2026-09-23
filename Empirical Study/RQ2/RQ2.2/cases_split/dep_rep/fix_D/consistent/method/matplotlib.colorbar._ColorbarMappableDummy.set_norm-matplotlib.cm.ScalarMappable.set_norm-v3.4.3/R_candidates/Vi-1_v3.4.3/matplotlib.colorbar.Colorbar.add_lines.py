    def add_lines(self, CS, erase=True):
        """
        Add the lines from a non-filled `~.contour.ContourSet` to the colorbar.

        Parameters
        ----------
        CS : `~.contour.ContourSet`
            The line positions are taken from the ContourSet levels. The
            ContourSet must not be filled.
        erase : bool, default: True
            Whether to remove any previously added lines.
        """
        if not isinstance(CS, contour.ContourSet) or CS.filled:
            raise ValueError('add_lines is only for a ContourSet of lines')
        tcolors = [c[0] for c in CS.tcolors]
        tlinewidths = [t[0] for t in CS.tlinewidths]
        # Wishlist: Make colorbar lines auto-follow changes in contour lines.
        super().add_lines(CS.levels, tcolors, tlinewidths, erase=erase)
