    def get_slice(self, slobj, axis=0):
        if axis >= self.ndim:
            raise IndexError("Requested axis not found in manager")

        if axis == 0:
            new_blocks = self._slice_take_blocks_ax0(slobj)
        else:
            slicer = [slice(None)] * (axis + 1)
            slicer[axis] = slobj
            slicer = tuple(slicer)
            new_blocks = [blk.getitem_block(slicer) for blk in self.blocks]

        new_axes = list(self.axes)
        new_axes[axis] = new_axes[axis][slobj]

        bm = self.__class__(new_blocks, new_axes, do_integrity_check=False)
        bm._consolidate_inplace()
        return bm
