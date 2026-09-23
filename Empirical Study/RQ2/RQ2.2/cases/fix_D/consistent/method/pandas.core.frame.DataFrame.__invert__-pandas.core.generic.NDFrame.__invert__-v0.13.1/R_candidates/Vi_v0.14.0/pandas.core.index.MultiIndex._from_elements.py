    @staticmethod
    def _from_elements(values, labels=None, levels=None, names=None,
                       sortorder=None):
        index = values.view(MultiIndex)
        index._set_levels(levels)
        index._set_labels(labels)
        index._set_names(names)
        index.sortorder = sortorder
        return index
