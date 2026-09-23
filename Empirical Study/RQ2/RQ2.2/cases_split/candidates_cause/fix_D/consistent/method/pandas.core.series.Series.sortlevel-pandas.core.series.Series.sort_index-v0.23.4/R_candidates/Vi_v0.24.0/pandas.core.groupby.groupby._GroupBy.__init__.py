    def __init__(self, obj, keys=None, axis=0, level=None,
                 grouper=None, exclusions=None, selection=None, as_index=True,
                 sort=True, group_keys=True, squeeze=False,
                 observed=False, **kwargs):

        self._selection = selection

        if isinstance(obj, NDFrame):
            obj._consolidate_inplace()

        self.level = level

        if not as_index:
            if not isinstance(obj, DataFrame):
                raise TypeError('as_index=False only valid with DataFrame')
            if axis != 0:
                raise ValueError('as_index=False only valid for axis=0')

        self.as_index = as_index
        self.keys = keys
        self.sort = sort
        self.group_keys = group_keys
        self.squeeze = squeeze
        self.observed = observed
        self.mutated = kwargs.pop('mutated', False)

        if grouper is None:
            from pandas.core.groupby.grouper import _get_grouper
            grouper, exclusions, obj = _get_grouper(obj, keys,
                                                    axis=axis,
                                                    level=level,
                                                    sort=sort,
                                                    observed=observed,
                                                    mutated=self.mutated)

        self.obj = obj
        self.axis = obj._get_axis_number(axis)
        self.grouper = grouper
        self.exclusions = set(exclusions) if exclusions else set()

        # we accept no other args
        validate_kwargs('group', kwargs, {})
