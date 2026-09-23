class MultiColSource(object):
    contains_aggregate = False

    def __init__(self, alias, targets, sources, field):
        self.targets, self.sources, self.field, self.alias = targets, sources, field, alias
        self.output_field = self.field

    def __repr__(self):
        return "{}({}, {})".format(
            self.__class__.__name__, self.alias, self.field)

    def relabeled_clone(self, relabels):
        return self.__class__(relabels.get(self.alias, self.alias),
                              self.targets, self.sources, self.field)
