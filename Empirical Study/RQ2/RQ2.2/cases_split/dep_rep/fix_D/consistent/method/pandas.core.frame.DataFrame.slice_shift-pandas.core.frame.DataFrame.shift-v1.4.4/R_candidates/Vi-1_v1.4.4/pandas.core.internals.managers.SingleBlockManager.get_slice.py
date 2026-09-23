    def get_slice(self, slobj: slice, axis: int = 0) -> SingleBlockManager:
        # Assertion disabled for performance
        # assert isinstance(slobj, slice), type(slobj)
        if axis >= self.ndim:
            raise IndexError("Requested axis not found in manager")

        blk = self._block
        array = blk._slice(slobj)
        bp = BlockPlacement(slice(0, len(array)))
        block = type(blk)(array, placement=bp, ndim=1)
        new_index = self.index._getitem_slice(slobj)
        return type(self)(block, new_index)
