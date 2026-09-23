    def __new__(cls, levels=None, labels=None, sortorder=None, names=None,
                copy=False, verify_integrity=True, _set_identity=True,
                name=None, **kwargs):

        # compat with Index
        if name is not None:
            names = name
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

        result = object.__new__(MultiIndex)

        # we've already validated levels and labels, so shortcut here
        result._set_levels(levels, copy=copy, validate=False)
        result._set_labels(labels, copy=copy, validate=False)

        if names is not None:
            # handles name validation
            result._set_names(names)

        if sortorder is not None:
            result.sortorder = int(sortorder)
        else:
            result.sortorder = sortorder

        if verify_integrity:
            result._verify_integrity()
        if _set_identity:
            result._reset_identity()
        return result
