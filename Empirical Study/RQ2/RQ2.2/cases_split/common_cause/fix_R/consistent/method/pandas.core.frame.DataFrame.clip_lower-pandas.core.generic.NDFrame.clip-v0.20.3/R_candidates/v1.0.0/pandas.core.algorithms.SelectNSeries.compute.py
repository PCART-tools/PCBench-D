    def compute(self, method):

        n = self.n
        dtype = self.obj.dtype
        if not self.is_valid_dtype_n_method(dtype):
            raise TypeError(f"Cannot use method '{method}' with dtype {dtype}")

        if n <= 0:
            return self.obj[[]]

        dropped = self.obj.dropna()

        # slow method
        if n >= len(self.obj):
            reverse_it = self.keep == "last" or method == "nlargest"
            ascending = method == "nsmallest"
            slc = np.s_[::-1] if reverse_it else np.s_[:]
            return dropped[slc].sort_values(ascending=ascending).head(n)

        # fast method
        arr, pandas_dtype = _ensure_data(dropped.values)
        if method == "nlargest":
            arr = -arr
            if is_integer_dtype(pandas_dtype):
                # GH 21426: ensure reverse ordering at boundaries
                arr -= 1

            elif is_bool_dtype(pandas_dtype):
                # GH 26154: ensure False is smaller than True
                arr = 1 - (-arr)

        if self.keep == "last":
            arr = arr[::-1]

        narr = len(arr)
        n = min(n, narr)

        kth_val = algos.kth_smallest(arr.copy(), n - 1)
        (ns,) = np.nonzero(arr <= kth_val)
        inds = ns[arr[ns].argsort(kind="mergesort")]

        if self.keep != "all":
            inds = inds[:n]

        if self.keep == "last":
            # reverse indices
            inds = narr - 1 - inds

        return dropped.iloc[inds]
