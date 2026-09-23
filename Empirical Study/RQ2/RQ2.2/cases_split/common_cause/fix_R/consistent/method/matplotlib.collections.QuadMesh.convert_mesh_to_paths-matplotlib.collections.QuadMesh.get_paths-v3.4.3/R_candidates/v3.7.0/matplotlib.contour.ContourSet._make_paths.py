    def _make_paths(self, segs, kinds):
        """
        Create and return Path objects for the specified segments and optional
        kind codes.  *segs* is a list of numpy arrays, each array is either a
        closed line loop or open line strip of 2D points with a shape of
        (npoints, 2).  *kinds* is either None or a list (with the same length
        as *segs*) of numpy arrays, each array is of shape (npoints,) and
        contains the kind codes for the corresponding line in *segs*.  If
        *kinds* is None then the Path constructor creates the kind codes
        assuming that the line is an open strip.
        """
        if kinds is None:
            return [mpath.Path(seg) for seg in segs]
        else:
            return [mpath.Path(seg, codes=kind) for seg, kind
                    in zip(segs, kinds)]
