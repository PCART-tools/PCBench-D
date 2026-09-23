    def compute(self, method):

        n = self.n
        dtype = self.obj.dtype
        if not self.is_valid_dtype_n_method(dtype):
            raise TypeError("Cannot use method '{method}' with "
                            "dtype {dtype}".format(method=method,
                                                   dtype=dtype))

        if n <= 0:
            return self.obj[[]]

        dropped = self.obj.dropna()

        # slow method
        if n >= len(self.obj):

            reverse_it = (self.keep == 'last' or method == 'nlargest')
            ascending = method == 'nsmallest'
            slc = np.s_[::-1] if reverse_it else np.s_[:]
            return dropped[slc].sort_values(ascending=ascending).head(n)

        # fast method
        arr, _, _ = _ensure_data(dropped.values)
        if method == 'nlargest':
            arr = -arr

        if self.keep == 'last':
            arr = arr[::-1]

        narr = len(arr)
        n = min(n, narr)

        kth_val = algos.kth_smallest(arr.copy(), n - 1)
        ns, = np.nonzero(arr <= kth_val)
        inds = ns[arr[ns].argsort(kind='mergesort')][:n]
        if self.keep == 'last':
            # reverse indices
            inds = narr - 1 - inds

        return dropped.iloc[inds]
