    def fast_apply(self, f, names):
        # must return keys::list, values::list, mutated::bool
        try:
            starts, ends = lib.generate_slices(self.slabels, self.ngroups)
        except Exception:
            # fails when all -1
            return [], True

        sdata = self._get_sorted_data()
        return reduction.apply_frame_axis0(sdata, f, names, starts, ends)
