    def __setstate__(self, aug_state):
        """Necessary for making this object picklable"""
        index_state = aug_state[:1]
        offset = aug_state[1]

        # for backwards compatibility
        if len(aug_state) > 2:
            tzinfo = aug_state[2]
        else:  # pragma: no cover
            tzinfo = None

        self.offset = offset
        self.tzinfo = tzinfo
        Index.__setstate__(self, *index_state)
