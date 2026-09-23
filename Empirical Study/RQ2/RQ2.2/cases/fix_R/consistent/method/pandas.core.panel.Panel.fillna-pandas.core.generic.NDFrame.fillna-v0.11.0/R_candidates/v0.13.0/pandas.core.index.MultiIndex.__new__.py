    def __new__(cls, levels=None, labels=None, sortorder=None, names=None,
                copy=False, verify_integrity=True):
        if levels is None or labels is None:
            raise TypeError("Must pass both levels and labels")
        if len(levels) != len(labels):
            raise ValueError('Length of levels and labels must be the same.')
        if len(levels) == 0:
            raise ValueError('Must pass non-zero number of levels/labels')
        if len(levels) == 1:
            if names:
                name = names[0]
            else:
                name = None

            return Index(levels[0], name=name, copy=True).take(labels[0])

        # v3, 0.8.0
        subarr = np.empty(0, dtype=object).view(cls)
        # we've already validated levels and labels, so shortcut here
        subarr._set_levels(levels, copy=copy, validate=False)
        subarr._set_labels(labels, copy=copy, validate=False)

        if names is not None:
            # handles name validation
            subarr._set_names(names)

        if sortorder is not None:
            subarr.sortorder = int(sortorder)
        else:
            subarr.sortorder = sortorder

        if verify_integrity:
            subarr._verify_integrity()

        return subarr
