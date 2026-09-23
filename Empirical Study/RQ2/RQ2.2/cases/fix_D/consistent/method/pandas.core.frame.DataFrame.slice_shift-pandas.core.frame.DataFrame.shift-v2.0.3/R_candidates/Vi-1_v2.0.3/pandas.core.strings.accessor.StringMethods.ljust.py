    @Appender(_shared_docs["str_pad"] % {"side": "right", "method": "ljust"})
    @forbid_nonstring_types(["bytes"])
    def ljust(self, width, fillchar: str = " "):
        return self.pad(width, side="right", fillchar=fillchar)
