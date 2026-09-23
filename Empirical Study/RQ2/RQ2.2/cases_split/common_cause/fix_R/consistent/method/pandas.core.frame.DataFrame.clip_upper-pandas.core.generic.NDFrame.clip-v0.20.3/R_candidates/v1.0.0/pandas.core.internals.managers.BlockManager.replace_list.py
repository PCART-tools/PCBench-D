    def replace_list(self, src_list, dest_list, inplace=False, regex=False):
        """ do a list replace """

        inplace = validate_bool_kwarg(inplace, "inplace")

        # figure out our mask a-priori to avoid repeated replacements
        values = self.as_array()

        def comp(s, regex=False):
            """
            Generate a bool array by perform an equality check, or perform
            an element-wise regular expression matching
            """
            if isna(s):
                return isna(values)
            if isinstance(s, (Timedelta, Timestamp)) and getattr(s, "tz", None) is None:

                return _compare_or_regex_search(
                    maybe_convert_objects(values), s.asm8, regex
                )
            return _compare_or_regex_search(values, s, regex)

        masks = [comp(s, regex) for i, s in enumerate(src_list)]

        result_blocks = []
        src_len = len(src_list) - 1
        for blk in self.blocks:

            # its possible to get multiple result blocks here
            # replace ALWAYS will return a list
            rb = [blk if inplace else blk.copy()]
            for i, (s, d) in enumerate(zip(src_list, dest_list)):
                # TODO: assert/validate that `d` is always a scalar?
                new_rb = []
                for b in rb:
                    m = masks[i][b.mgr_locs.indexer]
                    convert = i == src_len
                    result = b._replace_coerce(
                        mask=m,
                        to_replace=s,
                        value=d,
                        inplace=inplace,
                        convert=convert,
                        regex=regex,
                    )
                    if m.any() or convert:
                        new_rb = _extend_blocks(result, new_rb)
                    else:
                        new_rb.append(b)
                rb = new_rb
            result_blocks.extend(rb)

        bm = type(self)(result_blocks, self.axes)
        bm._consolidate_inplace()
        return bm
