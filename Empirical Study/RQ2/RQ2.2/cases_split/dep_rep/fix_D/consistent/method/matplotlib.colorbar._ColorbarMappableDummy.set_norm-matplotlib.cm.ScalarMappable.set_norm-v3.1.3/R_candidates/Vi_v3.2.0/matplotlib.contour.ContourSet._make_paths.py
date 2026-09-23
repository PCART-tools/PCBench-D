    def _make_paths(self, segs, kinds):
        if kinds is not None:
            return [mpath.Path(seg, codes=kind)
                    for seg, kind in zip(segs, kinds)]
        else:
            return [mpath.Path(seg) for seg in segs]
