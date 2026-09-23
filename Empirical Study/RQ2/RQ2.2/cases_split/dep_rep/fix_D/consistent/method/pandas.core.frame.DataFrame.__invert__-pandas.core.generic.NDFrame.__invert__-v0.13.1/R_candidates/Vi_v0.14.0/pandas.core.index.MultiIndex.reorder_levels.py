    def reorder_levels(self, order):
        """
        Rearrange levels using input order. May not drop or duplicate levels

        Parameters
        ----------
        """
        order = [self._get_level_number(i) for i in order]
        if len(order) != self.nlevels:
            raise AssertionError(('Length of order must be same as '
                                  'number of levels (%d), got %d')
                                 % (self.nlevels, len(order)))
        new_levels = [self.levels[i] for i in order]
        new_labels = [self.labels[i] for i in order]
        new_names = [self.names[i] for i in order]

        return MultiIndex(levels=new_levels, labels=new_labels,
                          names=new_names, verify_integrity=False)
