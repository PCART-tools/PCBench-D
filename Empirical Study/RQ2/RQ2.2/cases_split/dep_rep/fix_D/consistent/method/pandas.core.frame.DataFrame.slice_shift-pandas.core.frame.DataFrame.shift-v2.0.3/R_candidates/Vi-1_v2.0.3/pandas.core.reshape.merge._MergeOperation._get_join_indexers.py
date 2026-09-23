    def _get_join_indexers(self) -> tuple[npt.NDArray[np.intp], npt.NDArray[np.intp]]:
        """return the join indexers"""
        return get_join_indexers(
            self.left_join_keys, self.right_join_keys, sort=self.sort, how=self.how
        )
