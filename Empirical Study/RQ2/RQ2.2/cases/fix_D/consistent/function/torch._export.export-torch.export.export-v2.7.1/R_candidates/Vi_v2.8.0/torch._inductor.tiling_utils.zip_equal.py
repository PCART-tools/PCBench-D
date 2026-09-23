    def zip_equal(it1: Iterable[T], it2: Iterable[U]) -> Iterator[tuple[T, U]]:
        """
        Zip two iterables, raising ValueError if their lengths differ.
        """
        if len(it1) != len(it2):
            raise ValueError(f"Lengths differ: {len(it1)} != {len(it2)}")
        return zip(it1, it2)
