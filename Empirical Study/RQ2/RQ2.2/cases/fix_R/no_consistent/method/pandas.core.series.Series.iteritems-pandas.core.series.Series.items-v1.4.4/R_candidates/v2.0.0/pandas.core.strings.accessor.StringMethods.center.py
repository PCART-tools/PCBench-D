    @Appender(_shared_docs["str_pad"] % {"side": "left and right", "method": "center"})
    @forbid_nonstring_types(["bytes"])
    def center(self, width, fillchar: str = " "):
        return self.pad(width, side="both", fillchar=fillchar)
