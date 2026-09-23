    def __getitem__(self, index):
        out = 'getitem-' + tokenize(self, index)

        # Field access, e.g. x['a'] or x[['a', 'b']]
        if (isinstance(index, (str, unicode)) or
                (isinstance(index, list) and index and
                 all(isinstance(i, (str, unicode)) for i in index))):
            if isinstance(index, (str, unicode)):
                dt = self.dtype[index]
            else:
                dt = np.dtype([(name, self.dtype[name]) for name in index])

            if dt.shape:
                new_axis = list(range(self.ndim, self.ndim + len(dt.shape)))
                chunks = self.chunks + tuple((i,) for i in dt.shape)
                return self.map_blocks(getitem, index, dtype=dt.base, name=out,
                                       chunks=chunks, new_axis=new_axis)
            else:
                return self.map_blocks(getitem, index, dtype=dt, name=out)

        # Slicing
        if isinstance(index, Array):
            return slice_with_dask_array(self, index)

        if not isinstance(index, tuple):
            index = (index,)

        if any(isinstance(i, Array) for i in index):
            raise NotImplementedError("Indexing with a dask Array")

        if all(isinstance(i, slice) and i == slice(None) for i in index):
            return self

        dsk, chunks = slice_array(out, self.name, self.chunks, index)

        dsk2 = sharedict.merge(self.dask, (out, dsk))

        return Array(dsk2, out, chunks, dtype=self.dtype)
