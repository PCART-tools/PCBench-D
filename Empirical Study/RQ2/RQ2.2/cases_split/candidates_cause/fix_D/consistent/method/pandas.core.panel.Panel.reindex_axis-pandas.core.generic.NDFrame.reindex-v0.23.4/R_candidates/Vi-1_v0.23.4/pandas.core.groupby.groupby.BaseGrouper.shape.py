    @property
    def shape(self):
        return tuple(ping.ngroups for ping in self.groupings)
