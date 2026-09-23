    def replace_list(self, src_list, dest_list, inplace=False, regex=False,
                     mgr=None):
        """ do a list replace """

        inplace = validate_bool_kwarg(inplace, 'inplace')

        if mgr is None:
            mgr = self

        # figure out our mask a-priori to avoid repeated replacements
        values = self.as_matrix()

        def comp(s):
            if isnull(s):
                return isnull(values)
            return _maybe_compare(values, getattr(s, 'asm8', s), operator.eq)

        def _cast_scalar(block, scalar):
            dtype, val = infer_dtype_from_scalar(scalar, pandas_dtype=True)
            if not is_dtype_equal(block.dtype, dtype):
                dtype = find_common_type([block.dtype, dtype])
                block = block.astype(dtype)
                # use original value
                val = scalar

            return block, val

        masks = [comp(s) for i, s in enumerate(src_list)]

        result_blocks = []
        src_len = len(src_list) - 1
        for blk in self.blocks:

            # its possible to get multiple result blocks here
            # replace ALWAYS will return a list
            rb = [blk if inplace else blk.copy()]
            for i, (s, d) in enumerate(zip(src_list, dest_list)):
                new_rb = []
                for b in rb:
                    if b.dtype == np.object_:
                        convert = i == src_len
                        result = b.replace(s, d, inplace=inplace, regex=regex,
                                           mgr=mgr, convert=convert)
                        new_rb = _extend_blocks(result, new_rb)
                    else:
                        # get our mask for this element, sized to this
                        # particular block
                        m = masks[i][b.mgr_locs.indexer]
                        if m.any():
                            b, val = _cast_scalar(b, d)
                            new_rb.extend(b.putmask(m, val, inplace=True))
                        else:
                            new_rb.append(b)
                rb = new_rb
            result_blocks.extend(rb)

        bm = self.__class__(result_blocks, self.axes)
        bm._consolidate_inplace()
        return bm
