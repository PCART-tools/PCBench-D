    def _format_native_types(self, na_rep='nan', **kwargs):
        new_levels = []
        new_labels = []

        # go through the levels and format them
        for level, label in zip(self.levels, self.labels):
            level = level._format_native_types(na_rep=na_rep, **kwargs)
            # add nan values, if there are any
            mask = (label == -1)
            if mask.any():
                nan_index = len(level)
                level = np.append(level, na_rep)
                label = label.values()
                label[mask] = nan_index
            new_levels.append(level)
            new_labels.append(label)

        # reconstruct the multi-index
        mi = MultiIndex(levels=new_levels, labels=new_labels, names=self.names,
                        sortorder=self.sortorder, verify_integrity=False)

        return mi.values
