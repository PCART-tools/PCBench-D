    def get_bool_data(self, copy: bool = False) -> Self:
        """
        Select blocks that are bool-dtype and columns from object-dtype blocks
        that are all-bool.

        Parameters
        ----------
        copy : bool, default False
            Whether to copy the blocks
        """

        new_blocks = []

        for blk in self.blocks:
            if blk.dtype == bool:
                new_blocks.append(blk)

            elif blk.is_object:
                nbs = blk._split()
                new_blocks.extend(nb for nb in nbs if nb.is_bool)

        return self._combine(new_blocks, copy)
