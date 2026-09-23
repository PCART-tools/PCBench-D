    def get_new_columns(self):
        if self.value_columns is None:
            return self.removed_level

        stride = len(self.removed_level)
        width = len(self.value_columns)
        propagator = np.repeat(np.arange(width), stride)
        if isinstance(self.value_columns, MultiIndex):
            new_levels = self.value_columns.levels + (self.removed_level,)
            new_names = self.value_columns.names + (self.removed_name,)

            new_labels = [lab.take(propagator)
                          for lab in self.value_columns.labels]
            new_labels.append(np.tile(np.arange(stride), width))
        else:
            new_levels = [self.value_columns, self.removed_level]
            new_names = [self.value_columns.name, self.removed_name]

            new_labels = []

            new_labels.append(propagator)
            new_labels.append(np.tile(np.arange(stride), width))

        return MultiIndex(levels=new_levels, labels=new_labels,
                          names=new_names, verify_integrity=False)
