    @doc(_shared_docs["searchsorted"], klass="Categorical")
    def searchsorted(self, value, side="left", sorter=None):
        # searchsorted is very performance sensitive. By converting codes
        # to same dtype as self.codes, we get much faster performance.
        if is_scalar(value):
            codes = self.categories.get_loc(value)
            codes = self.codes.dtype.type(codes)
        else:
            locs = [self.categories.get_loc(x) for x in value]
            codes = np.array(locs, dtype=self.codes.dtype)
        return self.codes.searchsorted(codes, side=side, sorter=sorter)
