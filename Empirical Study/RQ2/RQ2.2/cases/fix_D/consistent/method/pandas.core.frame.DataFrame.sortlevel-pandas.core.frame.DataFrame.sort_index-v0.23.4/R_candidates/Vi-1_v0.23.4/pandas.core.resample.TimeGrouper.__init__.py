    def __init__(self, freq='Min', closed=None, label=None, how='mean',
                 axis=0, fill_method=None, limit=None, loffset=None,
                 kind=None, convention=None, base=0, **kwargs):
        # Check for correctness of the keyword arguments which would
        # otherwise silently use the default if misspelled
        if label not in {None, 'left', 'right'}:
            raise ValueError('Unsupported value {} for `label`'.format(label))
        if closed not in {None, 'left', 'right'}:
            raise ValueError('Unsupported value {} for `closed`'.format(
                closed))
        if convention not in {None, 'start', 'end', 'e', 's'}:
            raise ValueError('Unsupported value {} for `convention`'
                             .format(convention))

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
