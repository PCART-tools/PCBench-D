    def putmask(self, mask, new, align: bool = True):
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
            using_cow=using_copy_on_write(),
        )
