    def _iter_collection_uses_per_path(self, paths, all_transforms,
                                       offsets, facecolors, edgecolors):
        """
        Compute how many times each raw path object returned by
        `_iter_collection_raw_paths` would be used when calling
        `_iter_collection`. This is intended for the backend to decide
        on the tradeoff between using the paths in-line and storing
        them once and reusing. Rounds up in case the number of uses
        is not the same for every path.
        """
        Npaths = len(paths)
        if Npaths == 0 or len(facecolors) == len(edgecolors) == 0:
            return 0
        Npath_ids = max(Npaths, len(all_transforms))
        N = max(Npath_ids, len(offsets))
        return (N + Npath_ids - 1) // Npath_ids
