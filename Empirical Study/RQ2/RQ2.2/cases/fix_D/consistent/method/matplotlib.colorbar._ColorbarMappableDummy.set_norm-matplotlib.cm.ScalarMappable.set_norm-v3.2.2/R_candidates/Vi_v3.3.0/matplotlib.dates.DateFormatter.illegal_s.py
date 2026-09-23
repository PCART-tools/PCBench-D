    @cbook.deprecated("3.3")
    @property
    def illegal_s(self):
        return re.compile(r"((^|[^%])(%%)*%s)")
