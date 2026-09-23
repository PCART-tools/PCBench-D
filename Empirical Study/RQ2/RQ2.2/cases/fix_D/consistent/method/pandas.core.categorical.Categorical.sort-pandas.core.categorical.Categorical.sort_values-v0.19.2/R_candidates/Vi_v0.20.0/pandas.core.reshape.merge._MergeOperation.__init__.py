    def __init__(self, left, right, how='inner', on=None,
                 left_on=None, right_on=None, axis=1,
                 left_index=False, right_index=False, sort=True,
                 suffixes=('_x', '_y'), copy=True, indicator=False):
        self.left = self.orig_left = left
        self.right = self.orig_right = right
        self.how = how
        self.axis = axis

        self.on = com._maybe_make_list(on)
        self.left_on = com._maybe_make_list(left_on)
        self.right_on = com._maybe_make_list(right_on)

        self.copy = copy
        self.suffixes = suffixes
        self.sort = sort

        self.left_index = left_index
        self.right_index = right_index

        self.indicator = indicator

        if isinstance(self.indicator, compat.string_types):
            self.indicator_name = self.indicator
        elif isinstance(self.indicator, bool):
            self.indicator_name = '_merge' if self.indicator else None
        else:
            raise ValueError(
                'indicator option can only accept boolean or string arguments')

        if not isinstance(left, DataFrame):
            raise ValueError(
                'can not merge DataFrame with instance of '
                'type {0}'.format(type(left)))
        if not isinstance(right, DataFrame):
            raise ValueError(
                'can not merge DataFrame with instance of '
                'type {0}'.format(type(right)))

        if not is_bool(left_index):
            raise ValueError(
                'left_index parameter must be of type bool, not '
                '{0}'.format(type(left_index)))
        if not is_bool(right_index):
            raise ValueError(
                'right_index parameter must be of type bool, not '
                '{0}'.format(type(right_index)))

        # warn user when merging between different levels
        if left.columns.nlevels != right.columns.nlevels:
            msg = ('merging between different levels can give an unintended '
                   'result ({0} levels on the left, {1} on the right)')
            msg = msg.format(left.columns.nlevels, right.columns.nlevels)
            warnings.warn(msg, UserWarning)

        self._validate_specification()

        # note this function has side effects
        (self.left_join_keys,
         self.right_join_keys,
         self.join_names) = self._get_merge_keys()

        # validate the merge keys dtypes. We may need to coerce
        # to avoid incompat dtypes
        self._maybe_coerce_merge_keys()
