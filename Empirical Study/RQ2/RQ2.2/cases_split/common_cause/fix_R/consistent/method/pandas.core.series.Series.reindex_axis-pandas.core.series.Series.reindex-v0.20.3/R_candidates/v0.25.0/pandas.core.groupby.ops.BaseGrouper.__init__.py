    def __init__(
        self, axis, groupings, sort=True, group_keys=True, mutated=False, indexer=None
    ):
        self._filter_empty_groups = self.compressed = len(groupings) != 1
        self.axis = axis
        self.groupings = groupings
        self.sort = sort
        self.group_keys = group_keys
        self.mutated = mutated
        self.indexer = indexer
