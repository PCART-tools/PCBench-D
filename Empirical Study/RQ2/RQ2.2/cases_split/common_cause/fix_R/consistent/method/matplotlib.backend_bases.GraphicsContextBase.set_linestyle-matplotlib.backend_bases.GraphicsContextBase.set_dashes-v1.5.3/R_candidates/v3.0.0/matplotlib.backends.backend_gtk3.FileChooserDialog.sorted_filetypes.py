    @cbook.deprecated("3.0", alternative="sorted(self.filetypes.items())")
    def sorted_filetypes(self):
        return sorted(self.filetypes.items())
