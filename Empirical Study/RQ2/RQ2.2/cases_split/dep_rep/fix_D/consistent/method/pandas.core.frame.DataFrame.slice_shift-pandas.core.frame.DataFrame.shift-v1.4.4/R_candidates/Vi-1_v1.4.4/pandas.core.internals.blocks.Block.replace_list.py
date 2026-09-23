    @final
    def replace_list(
        self,
        src_list: Iterable[Any],
        dest_list: Sequence[Any],
        inplace: bool = False,
        regex: bool = False,
    ) -> list[Block]:
        """
        See BlockManager.replace_list docstring.
        """
        values = self.values

        # Exclude anything that we know we won't contain
        pairs = [
            (x, y) for x, y in zip(src_list, dest_list) if self._can_hold_element(x)
        ]
        if not len(pairs):
            # shortcut, nothing to replace
            return [self] if inplace else [self.copy()]

        src_len = len(pairs) - 1

        if is_string_dtype(values.dtype):
            # Calculate the mask once, prior to the call of comp
            # in order to avoid repeating the same computations
            mask = ~isna(values)
            masks = [
                compare_or_regex_search(values, s[0], regex=regex, mask=mask)
                for s in pairs
            ]
        else:
            # GH#38086 faster if we know we dont need to check for regex
            masks = [missing.mask_missing(values, s[0]) for s in pairs]

        # error: Argument 1 to "extract_bool_array" has incompatible type
        # "Union[ExtensionArray, ndarray, bool]"; expected "Union[ExtensionArray,
        # ndarray]"
        masks = [extract_bool_array(x) for x in masks]  # type: ignore[arg-type]

        rb = [self if inplace else self.copy()]
        for i, (src, dest) in enumerate(pairs):
            convert = i == src_len  # only convert once at the end
            new_rb: list[Block] = []

            # GH-39338: _replace_coerce can split a block into
            # single-column blocks, so track the index so we know
            # where to index into the mask
            for blk_num, blk in enumerate(rb):
                if len(rb) == 1:
                    m = masks[i]
                else:
                    mib = masks[i]
                    assert not isinstance(mib, bool)
                    m = mib[blk_num : blk_num + 1]

                result = blk._replace_coerce(
                    to_replace=src,
                    value=dest,
                    mask=m,
                    inplace=inplace,
                    regex=regex,
                )
                if convert and blk.is_object and not all(x is None for x in dest_list):
                    # GH#44498 avoid unwanted cast-back
                    result = extend_blocks(
                        [b.convert(numeric=False, copy=True) for b in result]
                    )
                new_rb.extend(result)
            rb = new_rb
        return rb
