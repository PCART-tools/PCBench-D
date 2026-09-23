    def _get_join_info(
        self,
    ) -> tuple[Index, npt.NDArray[np.intp] | None, npt.NDArray[np.intp] | None]:

        left_ax = self.left.axes[self.axis]
        right_ax = self.right.axes[self.axis]

        if self.left_index and self.right_index and self.how != "asof":
            join_index, left_indexer, right_indexer = left_ax.join(
                right_ax, how=self.how, return_indexers=True, sort=self.sort
            )

        elif self.right_index and self.how == "left":
            join_index, left_indexer, right_indexer = _left_join_on_index(
                left_ax, right_ax, self.left_join_keys, sort=self.sort
            )

        elif self.left_index and self.how == "right":
            join_index, right_indexer, left_indexer = _left_join_on_index(
                right_ax, left_ax, self.right_join_keys, sort=self.sort
            )
        else:
            (left_indexer, right_indexer) = self._get_join_indexers()

            if self.right_index:
                if len(self.left) > 0:
                    join_index = self._create_join_index(
                        self.left.index,
                        self.right.index,
                        left_indexer,
                        how="right",
                    )
                else:
                    join_index = self.right.index.take(right_indexer)
            elif self.left_index:
                if self.how == "asof":
                    # GH#33463 asof should always behave like a left merge
                    join_index = self._create_join_index(
                        self.left.index,
                        self.right.index,
                        left_indexer,
                        how="left",
                    )

                elif len(self.right) > 0:
                    join_index = self._create_join_index(
                        self.right.index,
                        self.left.index,
                        right_indexer,
                        how="left",
                    )
                else:
                    join_index = self.left.index.take(left_indexer)
            else:
                join_index = Index(np.arange(len(left_indexer)))

        if len(join_index) == 0:
            join_index = join_index.astype(object)
        return join_index, left_indexer, right_indexer
