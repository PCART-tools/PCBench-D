def pivot(self, index=None, columns=None, values=None):
    """
    See DataFrame.pivot
    """
    if values is None:
        cols = [columns] if index is None else [index, columns]
        append = index is None
        indexed = self.set_index(cols, append=append)
        return indexed.unstack(columns)
    else:
        if index is None:
            index = self.index
        else:
            index = self[index]
        indexed = Series(self[values].values,
                         index=MultiIndex.from_arrays([index, self[columns]]))
        return indexed.unstack(columns)
