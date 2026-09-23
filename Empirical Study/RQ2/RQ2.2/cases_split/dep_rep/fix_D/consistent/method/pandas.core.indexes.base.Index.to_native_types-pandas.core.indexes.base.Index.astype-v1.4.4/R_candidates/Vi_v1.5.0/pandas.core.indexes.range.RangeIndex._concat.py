    def _concat(self, indexes: list[Index], name: Hashable) -> Index:
        """
        Overriding parent method for the case of all RangeIndex instances.

        When all members of "indexes" are of type RangeIndex: result will be
        RangeIndex if possible, Int64Index otherwise. E.g.:
        indexes = [RangeIndex(3), RangeIndex(3, 6)] -> RangeIndex(6)
        indexes = [RangeIndex(3), RangeIndex(4, 6)] -> Int64Index([0,1,2,4,5])
        """
        if not all(isinstance(x, RangeIndex) for x in indexes):
            return super()._concat(indexes, name)

        elif len(indexes) == 1:
            return indexes[0]

        rng_indexes = cast(List[RangeIndex], indexes)

        start = step = next_ = None

        # Filter the empty indexes
        non_empty_indexes = [obj for obj in rng_indexes if len(obj)]

        for obj in non_empty_indexes:
            rng = obj._range

            if start is None:
                # This is set by the first non-empty index
                start = rng.start
                if step is None and len(rng) > 1:
                    step = rng.step
            elif step is None:
                # First non-empty index had only one element
                if rng.start == start:
                    values = np.concatenate([x._values for x in rng_indexes])
                    result = Int64Index(values)
                    return result.rename(name)

                step = rng.start - start

            non_consecutive = (step != rng.step and len(rng) > 1) or (
                next_ is not None and rng.start != next_
            )
            if non_consecutive:
                result = Int64Index(np.concatenate([x._values for x in rng_indexes]))
                return result.rename(name)

            if step is not None:
                next_ = rng[-1] + step

        if non_empty_indexes:
            # Get the stop value from "next" or alternatively
            # from the last non-empty index
            stop = non_empty_indexes[-1].stop if next_ is None else next_
            return RangeIndex(start, stop, step).rename(name)

        # Here all "indexes" had 0 length, i.e. were empty.
        # In this case return an empty range index.
        return RangeIndex(0, 0).rename(name)
