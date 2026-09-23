    def set_verts_and_codes(self, verts, codes):
        """This allows one to initialize vertices with path codes."""
        if len(verts) != len(codes):
            raise ValueError("'codes' must be a 1D list or array "
                             "with the same length of 'verts'")
        self._paths = []
        for xy, cds in zip(verts, codes):
            if len(xy):
                self._paths.append(mpath.Path(xy, cds))
            else:
                self._paths.append(mpath.Path(xy))
        self.stale = True
