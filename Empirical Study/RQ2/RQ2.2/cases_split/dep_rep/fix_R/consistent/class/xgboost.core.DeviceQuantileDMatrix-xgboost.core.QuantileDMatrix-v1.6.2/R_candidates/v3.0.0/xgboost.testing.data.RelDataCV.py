class RelDataCV(NamedTuple):
    """Simple data struct for holding a train-test split of a learning to rank dataset."""

    train: RelData
    test: RelData
    max_rel: int

    def is_binary(self) -> bool:
        """Whether the label consists of binary relevance degree."""
        return self.max_rel == 1
