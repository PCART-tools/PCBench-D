    def _check_indexing_error(self, key) -> None:
        if not is_hashable(key) or is_iterator(key):
            # We allow tuples if they are hashable, whereas other Index
            #  subclasses require scalar.
            # We have to explicitly exclude generators, as these are hashable.
            raise InvalidIndexError(key)
