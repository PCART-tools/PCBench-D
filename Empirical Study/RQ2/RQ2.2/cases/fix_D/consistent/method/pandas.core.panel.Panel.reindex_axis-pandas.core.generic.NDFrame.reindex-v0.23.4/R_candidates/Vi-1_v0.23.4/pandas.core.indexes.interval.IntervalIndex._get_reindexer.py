    def _get_reindexer(self, target):
        """
        Return an indexer for a target IntervalIndex with self
        """

        # find the left and right indexers
        lindexer = self._engine.get_indexer(target.left.values)
        rindexer = self._engine.get_indexer(target.right.values)

        # we want to return an indexer on the intervals
        # however, our keys could provide overlapping of multiple
        # intervals, so we iterate thru the indexers and construct
        # a set of indexers

        indexer = []
        n = len(self)

        for i, (lhs, rhs) in enumerate(zip(lindexer, rindexer)):

            target_value = target[i]

            # matching on the lhs bound
            if (lhs != -1 and
                    self.closed == 'right' and
                    target_value.left == self[lhs].right):
                lhs += 1

            # matching on the lhs bound
            if (rhs != -1 and
                    self.closed == 'left' and
                    target_value.right == self[rhs].left):
                rhs -= 1

            # not found
            if lhs == -1 and rhs == -1:
                indexer.append(np.array([-1]))

            elif rhs == -1:

                indexer.append(np.arange(lhs, n))

            elif lhs == -1:

                # care about left/right closed here
                value = self[i]

                # target.closed same as self.closed
                if self.closed == target.closed:
                    if target_value.left < value.left:
                        indexer.append(np.array([-1]))
                        continue

                # target.closed == 'left'
                elif self.closed == 'right':
                    if target_value.left <= value.left:
                        indexer.append(np.array([-1]))
                        continue

                # target.closed == 'right'
                elif self.closed == 'left':
                    if target_value.left <= value.left:
                        indexer.append(np.array([-1]))
                        continue

                indexer.append(np.arange(0, rhs + 1))

            else:
                indexer.append(np.arange(lhs, rhs + 1))

        return np.concatenate(indexer)
