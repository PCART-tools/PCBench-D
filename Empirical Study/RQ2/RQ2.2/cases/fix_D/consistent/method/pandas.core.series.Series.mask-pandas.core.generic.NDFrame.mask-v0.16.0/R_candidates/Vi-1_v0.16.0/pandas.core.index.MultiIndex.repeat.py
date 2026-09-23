    def repeat(self, n):
        return MultiIndex(levels=self.levels,
                          labels=[label.view(np.ndarray).repeat(n) for label in self.labels],
                          names=self.names,
                          sortorder=self.sortorder,
                          verify_integrity=False)
