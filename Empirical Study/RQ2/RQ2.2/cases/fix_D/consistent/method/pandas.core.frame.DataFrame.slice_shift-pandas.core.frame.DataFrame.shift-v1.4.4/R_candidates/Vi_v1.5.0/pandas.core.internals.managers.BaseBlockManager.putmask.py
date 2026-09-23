    def putmask(self, mask, new, align: bool = True):
        if (
            _using_copy_on_write()
            and self.refs is not None
            and not all(ref is None for ref in self.refs)
        ):
            # some reference -> copy full dataframe
            # TODO(CoW) this could be optimized to only copy the blocks that would
            # get modified
            self = self.copy()

        if align:
            align_keys = ["new", "mask"]
        else:
            align_keys = ["mask"]
            new = extract_array(new, extract_numpy=True)

        return self.apply(
            "putmask",
            align_keys=align_keys,
            mask=mask,
            new=new,
        )
