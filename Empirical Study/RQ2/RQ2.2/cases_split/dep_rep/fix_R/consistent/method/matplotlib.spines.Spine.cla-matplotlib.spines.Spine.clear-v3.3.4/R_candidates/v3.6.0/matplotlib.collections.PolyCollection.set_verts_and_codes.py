    def set_verts_and_codes(self, verts, codes):
        """Initialize vertices with path codes."""
        if len(verts) != len(codes):
            raise ValueError("'codes' must be a 1D list or array "
                             "with the same length of 'verts'")
        self._paths = [mpath.Path(xy, cds) if len(xy) else mpath.Path(xy)
                       for xy, cds in zip(verts, codes)]
        self.stale = True
