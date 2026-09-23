    def __init__(self, axis, groupings, sort=True, group_keys=True):
        self._filter_empty_groups = self.compressed = len(groupings) != 1
        self.axis, self.groupings, self.sort, self.group_keys = \
                axis, groupings, sort, group_keys
