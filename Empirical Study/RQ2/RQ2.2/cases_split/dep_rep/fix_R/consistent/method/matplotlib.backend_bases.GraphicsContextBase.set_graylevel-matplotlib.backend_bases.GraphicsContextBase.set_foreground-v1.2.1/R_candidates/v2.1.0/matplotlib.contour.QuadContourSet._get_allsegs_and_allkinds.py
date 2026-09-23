    def _get_allsegs_and_allkinds(self):
        """
        Create and return allsegs and allkinds by calling underlying C code.
        """
        allsegs = []
        if self.filled:
            lowers, uppers = self._get_lowers_and_uppers()
            allkinds = []
            for level, level_upper in zip(lowers, uppers):
                if self._corner_mask == 'legacy':
                    nlist = self.Cntr.trace(level, level_upper,
                                            nchunk=self.nchunk)
                    nseg = len(nlist) // 2
                    vertices = nlist[:nseg]
                    kinds = nlist[nseg:]
                else:
                    vertices, kinds = \
                        self._contour_generator.create_filled_contour(
                                                           level, level_upper)
                allsegs.append(vertices)
                allkinds.append(kinds)
        else:
            allkinds = None
            for level in self.levels:
                if self._corner_mask == 'legacy':
                    nlist = self.Cntr.trace(level)
                    nseg = len(nlist) // 2
                    vertices = nlist[:nseg]
                else:
                    vertices = self._contour_generator.create_contour(level)
                allsegs.append(vertices)
        return allsegs, allkinds
