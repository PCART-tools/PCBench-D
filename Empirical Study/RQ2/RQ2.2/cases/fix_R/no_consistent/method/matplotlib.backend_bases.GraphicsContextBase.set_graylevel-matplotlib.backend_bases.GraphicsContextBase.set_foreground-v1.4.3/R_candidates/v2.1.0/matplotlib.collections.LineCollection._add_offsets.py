    def _add_offsets(self, segs):
        offsets = self._uniform_offsets
        Nsegs = len(segs)
        Noffs = offsets.shape[0]
        if Noffs == 1:
            for i in range(Nsegs):
                segs[i] = segs[i] + i * offsets
        else:
            for i in range(Nsegs):
                io = i % Noffs
                segs[i] = segs[i] + offsets[io:io + 1]
        return segs
