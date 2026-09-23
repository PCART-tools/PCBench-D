    def _set_seq_locs(self, data, value):
        strdata = shim_array(data)
        new_s = [d for d in np.unique(strdata) if d not in self.seq]
        for ns in new_s:
            self.seq.append(ns)
            if ns in UnitData.spdict:
                self.locs.append(UnitData.spdict[ns])
            else:
                self.locs.append(value)
                value += 1
