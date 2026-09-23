    @cbook.deprecated("3.1")
    def iter_ticks(self):
        """
        Yield ``(Tick, location, label)`` tuples for major and minor ticks.
        """
        major_locs = self.get_majorticklocs()
        major_labels = self.major.formatter.format_ticks(major_locs)
        major_ticks = self.get_major_ticks(len(major_locs))
        yield from zip(major_ticks, major_locs, major_labels)
        minor_locs = self.get_minorticklocs()
        minor_labels = self.minor.formatter.format_ticks(minor_locs)
        minor_ticks = self.get_minor_ticks(len(minor_locs))
        yield from zip(minor_ticks, minor_locs, minor_labels)
