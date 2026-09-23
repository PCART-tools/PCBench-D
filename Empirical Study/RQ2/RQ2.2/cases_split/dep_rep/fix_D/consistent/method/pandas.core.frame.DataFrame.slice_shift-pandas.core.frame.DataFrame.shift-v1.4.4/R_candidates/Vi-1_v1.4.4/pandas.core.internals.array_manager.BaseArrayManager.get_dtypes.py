    def get_dtypes(self):
        return np.array([arr.dtype for arr in self.arrays], dtype="object")
