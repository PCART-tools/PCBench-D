    def get_duplicates(self):
        from collections import defaultdict
        counter = defaultdict(lambda: 0)
        for k in self.values:
            counter[k] += 1
        return sorted(k for k, v in compat.iteritems(counter) if v > 1)
