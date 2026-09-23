    def itertuples(self, index=True):
        """
        Iterate over rows of DataFrame as tuples, with index value
        as first element of the tuple
        """
        arrays = []
        if index:
            arrays.append(self.index)

        # use integer indexing because of possible duplicate column names
        arrays.extend(self.iloc[:, k] for k in range(len(self.columns)))
        return zip(*arrays)
