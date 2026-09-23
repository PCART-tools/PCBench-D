    def to_native_types(self, slicer=None, na_rep="nan", quoting=None, **kwargs):
        """ convert to our native types format, slicing if desired """
        values = self.get_values()

        if slicer is not None:
            values = values[:, slicer]
        mask = isna(values)
        itemsize = writers.word_len(na_rep)

        if not self.is_object and not quoting and itemsize:
            values = values.astype(f"<U{itemsize}")
        else:
            values = np.array(values, dtype="object")

        values[mask] = na_rep
        return values
