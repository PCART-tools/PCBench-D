    def get_new_index(self):
        result_codes = [lab.take(self.compressor)
                        for lab in self.sorted_labels[:-1]]

        # construct the new index
        if len(self.new_index_levels) == 1:
            lev, lab = self.new_index_levels[0], result_codes[0]
            if (lab == -1).any():
                lev = lev.insert(len(lev), lev._na_value)
            return lev.take(lab)

        return MultiIndex(levels=self.new_index_levels, codes=result_codes,
                          names=self.new_index_names, verify_integrity=False)
