    def _apply_filter(self, indices, dropna):
        if len(indices) == 0:
            indices = []
        else:
            indices = np.sort(np.concatenate(indices))
        if dropna:
            filtered = self.obj.take(indices)
        else:
            mask = np.empty(len(self.obj.index), dtype=bool)
            mask.fill(False)
            mask[indices.astype(int)] = True
            # mask fails to broadcast when passed to where; broadcast manually.
            mask = np.tile(mask, list(self.obj.shape[1:]) + [1]).T
            filtered = self.obj.where(mask)  # Fill with NaNs.
        return filtered
