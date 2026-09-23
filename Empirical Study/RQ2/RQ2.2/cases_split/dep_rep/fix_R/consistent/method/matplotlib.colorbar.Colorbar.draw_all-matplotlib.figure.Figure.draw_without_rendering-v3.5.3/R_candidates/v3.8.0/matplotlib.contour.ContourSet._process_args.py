    def _process_args(self, *args, **kwargs):
        """
        Process *args* and *kwargs*; override in derived classes.

        Must set self.levels, self.zmin and self.zmax, and update axes limits.
        """
        self.levels = args[0]
        allsegs = args[1]
        allkinds = args[2] if len(args) > 2 else None
        self.zmax = np.max(self.levels)
        self.zmin = np.min(self.levels)

        if allkinds is None:
            allkinds = [[None] * len(segs) for segs in allsegs]

        # Check lengths of levels and allsegs.
        if self.filled:
            if len(allsegs) != len(self.levels) - 1:
                raise ValueError('must be one less number of segments as '
                                 'levels')
        else:
            if len(allsegs) != len(self.levels):
                raise ValueError('must be same number of segments as levels')

        # Check length of allkinds.
        if len(allkinds) != len(allsegs):
            raise ValueError('allkinds has different length to allsegs')

        # Determine x, y bounds and update axes data limits.
        flatseglist = [s for seg in allsegs for s in seg]
        points = np.concatenate(flatseglist, axis=0)
        self._mins = points.min(axis=0)
        self._maxs = points.max(axis=0)

        # Each entry in (allsegs, allkinds) is a list of (segs, kinds): segs is a list
        # of (N, 2) arrays of xy coordinates, kinds is a list of arrays of corresponding
        # pathcodes.  However, kinds can also be None; in which case all paths in that
        # list are codeless (this case is normalized above).  These lists are used to
        # construct paths, which then get concatenated.
        self._paths = [Path.make_compound_path(*map(Path, segs, kinds))
                       for segs, kinds in zip(allsegs, allkinds)]

        return kwargs
