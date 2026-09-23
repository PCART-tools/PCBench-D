    @Appender(_interval_shared_docs["contains"] % _shared_docs_kwargs)
    def contains(self, other):
        if isinstance(other, Interval):
            raise NotImplementedError("contains not implemented for two intervals")

        return (self.left < other if self.open_left else self.left <= other) & (
            other < self.right if self.open_right else other <= self.right
        )
