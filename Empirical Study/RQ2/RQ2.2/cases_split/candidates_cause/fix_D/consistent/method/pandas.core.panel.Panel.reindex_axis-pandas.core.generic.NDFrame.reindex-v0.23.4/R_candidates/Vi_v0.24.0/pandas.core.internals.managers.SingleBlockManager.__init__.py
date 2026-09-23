    def __init__(self, block, axis, do_integrity_check=False, fastpath=False):

        if isinstance(axis, list):
            if len(axis) != 1:
                raise ValueError("cannot create SingleBlockManager with more "
                                 "than 1 axis")
            axis = axis[0]

        # passed from constructor, single block, single axis
        if fastpath:
            self.axes = [axis]
            if isinstance(block, list):

                # empty block
                if len(block) == 0:
                    block = [np.array([])]
                elif len(block) != 1:
                    raise ValueError('Cannot create SingleBlockManager with '
                                     'more than 1 block')
                block = block[0]
        else:
            self.axes = [ensure_index(axis)]

            # create the block here
            if isinstance(block, list):

                # provide consolidation to the interleaved_dtype
                if len(block) > 1:
                    dtype = _interleaved_dtype(block)
                    block = [b.astype(dtype) for b in block]
                    block = _consolidate(block)

                if len(block) != 1:
                    raise ValueError('Cannot create SingleBlockManager with '
                                     'more than 1 block')
                block = block[0]

        if not isinstance(block, Block):
            block = make_block(block, placement=slice(0, len(axis)), ndim=1)

        self.blocks = [block]
