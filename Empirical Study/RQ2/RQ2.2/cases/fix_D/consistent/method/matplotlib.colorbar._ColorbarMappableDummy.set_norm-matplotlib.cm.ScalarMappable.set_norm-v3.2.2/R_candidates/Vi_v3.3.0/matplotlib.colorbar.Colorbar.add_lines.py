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
        # The following was an attempt to get the colorbar lines
        # to follow subsequent changes in the contour lines,
        # but more work is needed: specifically, a careful
        # look at event sequences, and at how
        # to make one object track another automatically.
        #tcolors = [col.get_colors()[0] for col in CS.collections]
        #tlinewidths = [col.get_linewidth()[0] for lw in CS.collections]
        ColorbarBase.add_lines(self, CS.levels, tcolors, tlinewidths,
                               erase=erase)
