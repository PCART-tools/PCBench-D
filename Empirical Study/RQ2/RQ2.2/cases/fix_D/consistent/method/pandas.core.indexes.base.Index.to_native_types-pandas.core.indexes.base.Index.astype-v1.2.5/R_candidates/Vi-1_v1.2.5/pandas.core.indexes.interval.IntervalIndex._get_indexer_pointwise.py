    def _get_indexer_pointwise(self, target: Index) -> Tuple[np.ndarray, np.ndarray]:
        """
        pointwise implementation for get_indexer and get_indexer_non_unique.
        """
        indexer, missing = [], []
        for i, key in enumerate(target):
            try:
                locs = self.get_loc(key)
                if isinstance(locs, slice):
                    # Only needed for get_indexer_non_unique
                    locs = np.arange(locs.start, locs.stop, locs.step, dtype="intp")
                locs = np.array(locs, ndmin=1)
            except KeyError:
                missing.append(i)
                locs = np.array([-1])
            except InvalidIndexError as err:
                # i.e. non-scalar key
                raise TypeError(key) from err

            indexer.append(locs)

        indexer = np.concatenate(indexer)
        return ensure_platform_int(indexer), ensure_platform_int(missing)
