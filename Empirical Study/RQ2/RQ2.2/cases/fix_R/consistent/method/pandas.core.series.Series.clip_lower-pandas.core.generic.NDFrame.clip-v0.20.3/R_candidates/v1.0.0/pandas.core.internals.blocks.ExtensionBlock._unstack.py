    def _unstack(self, unstacker_func, new_columns, n_rows, fill_value):
        # ExtensionArray-safe unstack.
        # We override ObjectBlock._unstack, which unstacks directly on the
        # values of the array. For EA-backed blocks, this would require
        # converting to a 2-D ndarray of objects.
        # Instead, we unstack an ndarray of integer positions, followed by
        # a `take` on the actual values.
        dummy_arr = np.arange(n_rows)
        dummy_unstacker = functools.partial(unstacker_func, fill_value=-1)
        unstacker = dummy_unstacker(dummy_arr)

        new_placement, new_values, mask = self._get_unstack_items(
            unstacker, new_columns
        )

        blocks = [
            self.make_block_same_class(
                self.values.take(indices, allow_fill=True, fill_value=fill_value),
                [place],
            )
            for indices, place in zip(new_values.T, new_placement)
        ]
        return blocks, mask
