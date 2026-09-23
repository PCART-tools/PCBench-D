    @property
    def levels(self):
        return [ping.group_index for ping in self.groupings]
