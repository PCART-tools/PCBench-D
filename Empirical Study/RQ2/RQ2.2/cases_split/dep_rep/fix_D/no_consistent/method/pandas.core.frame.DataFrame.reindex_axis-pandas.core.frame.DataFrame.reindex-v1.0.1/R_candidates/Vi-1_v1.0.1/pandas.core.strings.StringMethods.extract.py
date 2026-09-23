    @copy(str_extract)
    @forbid_nonstring_types(["bytes"])
    def extract(self, pat, flags=0, expand=True):
        return str_extract(self, pat, flags=flags, expand=expand)
