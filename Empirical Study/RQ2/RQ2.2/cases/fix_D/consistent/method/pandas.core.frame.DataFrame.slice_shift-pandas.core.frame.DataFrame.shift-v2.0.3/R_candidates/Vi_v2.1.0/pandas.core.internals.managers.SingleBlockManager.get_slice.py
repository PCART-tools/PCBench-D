    def get_slice(self, slobj: slice, axis: AxisInt = 0) -> SingleBlockManager:
        # Assertion disabled for performance
        # assert isinstance(slobj, slice), type(slobj)
        if axis >= self.ndim:
            raise IndexError("Requested axis not found in manager")

        blk = self._block
        array = blk.values[slobj]
        bp = BlockPlacement(slice(0, len(array)))
        # TODO this method is only used in groupby SeriesSplitter at the moment,
        # so passing refs is not yet covered by the tests
        block = type(blk)(array, placement=bp, ndim=1, refs=blk.refs)
        new_index = self.index._getitem_slice(slobj)
        return type(self)(block, new_index)
