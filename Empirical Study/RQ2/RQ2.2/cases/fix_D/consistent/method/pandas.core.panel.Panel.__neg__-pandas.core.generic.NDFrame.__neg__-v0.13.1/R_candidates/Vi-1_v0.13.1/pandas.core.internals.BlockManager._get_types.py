    def _get_types(self, f):
        """ return a list of the f per item """
        self._consolidate_inplace()

        # unique
        if self.items.is_unique:
            l = [ None ] * len(self.items)
            for b in self.blocks:
                v = f(b)
                for rl in b.ref_locs:
                    l[rl] = v
            return l

        # non-unique
        ref_locs = self._set_ref_locs()
        return [ f(ref_locs[i][0]) for i, item in enumerate(self.items) ]
