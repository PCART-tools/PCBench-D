    @staticmethod
    def _from_elements(values, labels=None, levels=None, names=None,
                       sortorder=None):
        return MultiIndex(levels, labels, names, sortorder=sortorder)
