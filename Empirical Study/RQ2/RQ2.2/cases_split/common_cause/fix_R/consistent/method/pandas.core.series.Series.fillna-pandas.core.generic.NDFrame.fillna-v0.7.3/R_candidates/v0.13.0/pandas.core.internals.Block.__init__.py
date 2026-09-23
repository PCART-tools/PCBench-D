    def __init__(self, values, items, ref_items, ndim=None, fastpath=False,
                 placement=None):

        if ndim is None:
            ndim = values.ndim

        if values.ndim != ndim:
            raise ValueError('Wrong number of dimensions')

        if len(items) != len(values):
            raise ValueError('Wrong number of items passed %d, indices imply '
                             '%d' % (len(items), len(values)))

        self.set_ref_locs(placement)
        self.values = values
        self.ndim = ndim

        if fastpath:
            self.items = items
            self.ref_items = ref_items
        else:
            self.items = _ensure_index(items)
            self.ref_items = _ensure_index(ref_items)
