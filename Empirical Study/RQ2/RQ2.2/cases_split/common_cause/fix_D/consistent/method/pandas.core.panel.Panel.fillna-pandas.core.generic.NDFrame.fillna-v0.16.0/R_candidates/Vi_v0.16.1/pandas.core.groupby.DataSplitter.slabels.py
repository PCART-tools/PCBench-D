    @cache_readonly
    def slabels(self):
        # Sorted labels
        return com.take_nd(self.labels, self.sort_idx, allow_fill=False)
