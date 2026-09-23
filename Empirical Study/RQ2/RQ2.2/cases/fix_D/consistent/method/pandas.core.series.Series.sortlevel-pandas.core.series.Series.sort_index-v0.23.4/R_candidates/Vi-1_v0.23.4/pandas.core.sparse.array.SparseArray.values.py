    @property
    def values(self):
        """
        Dense values
        """
        output = np.empty(len(self), dtype=self.dtype)
        int_index = self.sp_index.to_int_index()
        output.fill(self.fill_value)
        output.put(int_index.indices, self)
        return output
