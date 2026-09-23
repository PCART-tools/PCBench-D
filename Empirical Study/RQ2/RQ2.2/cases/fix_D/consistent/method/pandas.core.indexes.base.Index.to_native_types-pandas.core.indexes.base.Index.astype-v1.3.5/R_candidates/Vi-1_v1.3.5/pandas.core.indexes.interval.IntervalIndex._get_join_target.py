    def _get_join_target(self) -> np.ndarray:
        # constructing tuples is much faster than constructing Intervals
        tups = list(zip(self.left, self.right))
        target = construct_1d_object_array_from_listlike(tups)
        return target
