    def __init__(self, freq='Min', closed=None, label=None, how='mean',
                 nperiods=None, axis=0,
                 fill_method=None, limit=None, loffset=None, kind=None,
                 convention=None, base=0, **kwargs):
        freq = to_offset(freq)

        end_types = set(['M', 'A', 'Q', 'BM', 'BA', 'BQ', 'W'])
        rule = freq.rule_code
        if (rule in end_types or
                ('-' in rule and rule[:rule.find('-')] in end_types)):
            if closed is None:
                closed = 'right'
            if label is None:
                label = 'right'
        else:
            if closed is None:
                closed = 'left'
            if label is None:
                label = 'left'

        self.closed = closed
        self.label = label
        self.nperiods = nperiods
        self.kind = kind

        self.convention = convention or 'E'
        self.convention = self.convention.lower()

        if isinstance(loffset, compat.string_types):
            loffset = to_offset(loffset)
        self.loffset = loffset

        self.how = how
        self.fill_method = fill_method
        self.limit = limit
        self.base = base

        # always sort time groupers
        kwargs['sort'] = True

        super(TimeGrouper, self).__init__(freq=freq, axis=axis, **kwargs)
