    def replace_list(self, src_lst, dest_lst, inplace=False, regex=False):
        """ do a list replace """

        # figure out our mask a-priori to avoid repeated replacements
        values = self.as_matrix()

        def comp(s):
            if isnull(s):
                return isnull(values)
            return values == getattr(s, 'asm8', s)
        masks = [comp(s) for i, s in enumerate(src_lst)]

        result_blocks = []
        for blk in self.blocks:

            # its possible to get multiple result blocks here
            # replace ALWAYS will return a list
            rb = [blk if inplace else blk.copy()]
            for i, (s, d) in enumerate(zip(src_lst, dest_lst)):
                new_rb = []
                for b in rb:
                    if b.dtype == np.object_:
                        result = b.replace(s, d, inplace=inplace,
                                           regex=regex)
                        if isinstance(result, list):
                            new_rb.extend(result)
                        else:
                            new_rb.append(result)
                    else:
                        # get our mask for this element, sized to this
                        # particular block
                        m = masks[i][b.ref_locs]
                        if m.any():
                            new_rb.extend(b.putmask(m, d, inplace=True))
                        else:
                            new_rb.append(b)
                rb = new_rb
            result_blocks.extend(rb)

        bm = self.__class__(result_blocks, self.axes)
        bm._consolidate_inplace()
        return bm
