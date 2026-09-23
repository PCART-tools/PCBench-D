    def __init__(self, values, items, ref_items, ndim=None, fastpath=False,
                 placement=None):

        # kludgetastic
        if ndim is not None:
            if ndim == 1:
                ndim = 1
            elif ndim > 2:
                ndim = ndim
        else:
            if len(items) != 1:
                ndim = 1
            else:
                ndim = 2
        self.ndim = ndim

        self._ref_locs = None
        self.values = values
        if fastpath:
            self.items = items
            self.ref_items = ref_items
        else:
            self.items = _ensure_index(items)
            self.ref_items = _ensure_index(ref_items)
