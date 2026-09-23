    def __iter__(self):
        if np.issubdtype(self.dtype, np.floating):
            boxer = float
        elif np.issubdtype(self.dtype, np.integer):
            boxer = int
        else:
            boxer = lambda x: x

        for i in range(len(self)):
            r = self._get_val_at(i)

            # box em
            yield boxer(r)
