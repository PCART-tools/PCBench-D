    def _slice_take_blocks_ax0(self, slice_or_indexer, fill_tuple=None):
        """
        Slice/take blocks along axis=0.

        Overloaded for SingleBlock

        Returns
        -------
        new_blocks : list of Block

        """

        allow_fill = fill_tuple is not None

        sl_type, slobj, sllen = _preprocess_slice_or_indexer(
            slice_or_indexer, self.shape[0], allow_fill=allow_fill)

        if self._is_single_block:
            blk = self.blocks[0]

            if sl_type in ('slice', 'mask'):
                return [blk.getitem_block(slobj, new_mgr_locs=slice(0, sllen))]
            elif not allow_fill or self.ndim == 1:
                if allow_fill and fill_tuple[0] is None:
                    _, fill_value = _maybe_promote(blk.dtype)
                    fill_tuple = (fill_value, )

                return [blk.take_nd(slobj, axis=0,
                                    new_mgr_locs=slice(0, sllen),
                                    fill_tuple=fill_tuple)]

        if sl_type in ('slice', 'mask'):
            blknos = self._blknos[slobj]
            blklocs = self._blklocs[slobj]
        else:
            blknos = algos.take_1d(self._blknos, slobj, fill_value=-1,
                                   allow_fill=allow_fill)
            blklocs = algos.take_1d(self._blklocs, slobj, fill_value=-1,
                                    allow_fill=allow_fill)

        # When filling blknos, make sure blknos is updated before appending to
        # blocks list, that way new blkno is exactly len(blocks).
        #
        # FIXME: mgr_groupby_blknos must return mgr_locs in ascending order,
        # pytables serialization will break otherwise.
        blocks = []
        for blkno, mgr_locs in _get_blkno_placements(blknos, len(self.blocks),
                                                     group=True):
            if blkno == -1:
                # If we've got here, fill_tuple was not None.
                fill_value = fill_tuple[0]

                blocks.append(self._make_na_block(placement=mgr_locs,
                                                  fill_value=fill_value))
            else:
                blk = self.blocks[blkno]

                # Otherwise, slicing along items axis is necessary.
                if not blk._can_consolidate:
                    # A non-consolidatable block, it's easy, because there's
                    # only one item and each mgr loc is a copy of that single
                    # item.
                    for mgr_loc in mgr_locs:
                        newblk = blk.copy(deep=True)
                        newblk.mgr_locs = slice(mgr_loc, mgr_loc + 1)
                        blocks.append(newblk)

                else:
                    blocks.append(blk.take_nd(blklocs[mgr_locs.indexer],
                                              axis=0, new_mgr_locs=mgr_locs,
                                              fill_tuple=None))

        return blocks
