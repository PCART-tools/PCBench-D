    def where(self: T, other, cond, align: bool) -> T:
        if align:
            align_keys = ["other", "cond"]
        else:
            align_keys = ["cond"]
            other = extract_array(other, extract_numpy=True)

        return self.apply(
            "where",
            align_keys=align_keys,
            other=other,
            cond=cond,
            using_cow=using_copy_on_write(),
        )
