    @property
    def shape(self) -> Shape:
        return tuple(ping.ngroups for ping in self.groupings)
