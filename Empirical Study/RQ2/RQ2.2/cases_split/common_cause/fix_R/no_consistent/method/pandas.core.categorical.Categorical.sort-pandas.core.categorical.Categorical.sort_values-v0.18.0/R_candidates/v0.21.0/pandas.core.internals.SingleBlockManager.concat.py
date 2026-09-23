    def concat(self, to_concat, new_axis):
        """
        Concatenate a list of SingleBlockManagers into a single
        SingleBlockManager.

        Used for pd.concat of Series objects with axis=0.

        Parameters
        ----------
        to_concat : list of SingleBlockManagers
        new_axis : Index of the result

        Returns
        -------
        SingleBlockManager

        """
        non_empties = [x for x in to_concat if len(x) > 0]

        # check if all series are of the same block type:
        if len(non_empties) > 0:
            blocks = [obj.blocks[0] for obj in non_empties]

            if all([type(b) is type(blocks[0]) for b in blocks[1:]]):  # noqa
                new_block = blocks[0].concat_same_type(blocks)
            else:
                values = [x.values for x in blocks]
                values = _concat._concat_compat(values)
                new_block = make_block(
                    values, placement=slice(0, len(values), 1))
        else:
            values = [x._block.values for x in to_concat]
            values = _concat._concat_compat(values)
            new_block = make_block(
                values, placement=slice(0, len(values), 1))

        mgr = SingleBlockManager(new_block, new_axis)
        return mgr
