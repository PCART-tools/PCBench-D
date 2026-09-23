    def __iter__(self):
        """
        Iterate over each of the disjoint sets as a list.

        The iterator is invalid if interleaved with calls to join().
        """
        self.clean()
        token = object()

        # Mark each group as we come across if by appending a token,
        # and don't yield it twice
        for group in six.itervalues(self._mapping):
            if group[-1] is not token:
                yield [x() for x in group]
                group.append(token)

        # Cleanup the tokens
        for group in six.itervalues(self._mapping):
            if group[-1] is token:
                del group[-1]
