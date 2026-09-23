    def nth(self, n):
        def picker(arr):
            arr = arr[notnull(arr)]
            if len(arr) >= n + 1:
                return arr.iget(n)
            else:
                return np.nan
        return self.agg(picker)
