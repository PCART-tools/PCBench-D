def pivot(self, index=None, columns=None, values=None):
    """
    See DataFrame.pivot
    """
    if values is None:
        indexed = self.set_index([index, columns])
        return indexed.unstack(columns)
    else:
        indexed = Series(self[values].values,
                         index=MultiIndex.from_arrays([self[index],
                                                       self[columns]]))
        return indexed.unstack(columns)
