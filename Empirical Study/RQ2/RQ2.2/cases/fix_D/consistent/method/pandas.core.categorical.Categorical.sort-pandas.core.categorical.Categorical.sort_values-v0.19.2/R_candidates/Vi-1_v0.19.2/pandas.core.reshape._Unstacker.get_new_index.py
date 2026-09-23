    def get_new_index(self):
        result_labels = [lab.take(self.compressor)
                         for lab in self.sorted_labels[:-1]]

        # construct the new index
        if len(self.new_index_levels) == 1:
            lev, lab = self.new_index_levels[0], result_labels[0]
            if (lab == -1).any():
                lev = lev.insert(len(lev), _get_na_value(lev.dtype.type))
            return lev.take(lab)

        return MultiIndex(levels=self.new_index_levels, labels=result_labels,
                          names=self.new_index_names, verify_integrity=False)
