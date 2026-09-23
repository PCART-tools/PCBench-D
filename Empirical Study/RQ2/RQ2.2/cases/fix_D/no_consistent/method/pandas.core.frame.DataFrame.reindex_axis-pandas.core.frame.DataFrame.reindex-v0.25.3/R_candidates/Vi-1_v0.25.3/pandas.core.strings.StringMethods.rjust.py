    @Appender(_shared_docs["str_pad"] % dict(side="left", method="rjust"))
    @forbid_nonstring_types(["bytes"])
    def rjust(self, width, fillchar=" "):
        return self.pad(width, side="left", fillchar=fillchar)
