
    def convert_objects(self):
        """
        Attempt to infer better dtype for object columns

        Returns
        -------
        converted : DataFrame
        """
        new_data = {}

        # TODO: could be more efficient taking advantage of the block
        for col, s in self.iteritems():
            if s.dtype == np.object_:
                new_data[col] = lib.maybe_convert_objects(s)
            else:
                new_data[col] = s

        return DataFrame(new_data, index=self.index, columns=self.columns)
