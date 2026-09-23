    @property
    def has_duplicates(self):
        """
        Return True if there are no unique groups
        """
        # has duplicates
        shape = [len(lev) for lev in self.levels]
        group_index = np.zeros(len(self), dtype='i8')
        for i in range(len(shape)):
            stride = np.prod([x for x in shape[i + 1:]], dtype='i8')
            group_index += self.labels[i] * stride

        if len(np.unique(group_index)) < len(group_index):
            return True

        return False
