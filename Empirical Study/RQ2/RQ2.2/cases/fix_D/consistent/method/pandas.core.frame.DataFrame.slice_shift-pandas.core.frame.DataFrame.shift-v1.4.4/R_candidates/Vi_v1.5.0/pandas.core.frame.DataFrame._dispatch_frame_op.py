    def _dispatch_frame_op(self, right, func: Callable, axis: int | None = None):
        """
        Evaluate the frame operation func(left, right) by evaluating
        column-by-column, dispatching to the Series implementation.

        Parameters
        ----------
        right : scalar, Series, or DataFrame
        func : arithmetic or comparison operator
        axis : {None, 0, 1}

        Returns
        -------
        DataFrame
        """
        # Get the appropriate array-op to apply to each column/block's values.
        array_op = ops.get_array_op(func)

        right = lib.item_from_zerodim(right)
        if not is_list_like(right):
            # i.e. scalar, faster than checking np.ndim(right) == 0
            with np.errstate(all="ignore"):
                bm = self._mgr.apply(array_op, right=right)
            return self._constructor(bm)

        elif isinstance(right, DataFrame):
            assert self.index.equals(right.index)
            assert self.columns.equals(right.columns)
            # TODO: The previous assertion `assert right._indexed_same(self)`
            #  fails in cases with empty columns reached via
            #  _frame_arith_method_with_reindex

            # TODO operate_blockwise expects a manager of the same type
            with np.errstate(all="ignore"):
                bm = self._mgr.operate_blockwise(
                    # error: Argument 1 to "operate_blockwise" of "ArrayManager" has
                    # incompatible type "Union[ArrayManager, BlockManager]"; expected
                    # "ArrayManager"
                    # error: Argument 1 to "operate_blockwise" of "BlockManager" has
                    # incompatible type "Union[ArrayManager, BlockManager]"; expected
                    # "BlockManager"
                    right._mgr,  # type: ignore[arg-type]
                    array_op,
                )
            return self._constructor(bm)

        elif isinstance(right, Series) and axis == 1:
            # axis=1 means we want to operate row-by-row
            assert right.index.equals(self.columns)

            right = right._values
            # maybe_align_as_frame ensures we do not have an ndarray here
            assert not isinstance(right, np.ndarray)

            with np.errstate(all="ignore"):
                arrays = [
                    array_op(_left, _right)
                    for _left, _right in zip(self._iter_column_arrays(), right)
                ]

        elif isinstance(right, Series):
            assert right.index.equals(self.index)  # Handle other cases later
            right = right._values

            with np.errstate(all="ignore"):
                arrays = [array_op(left, right) for left in self._iter_column_arrays()]

        else:
            # Remaining cases have less-obvious dispatch rules
            raise NotImplementedError(right)

        return type(self)._from_arrays(
            arrays, self.columns, self.index, verify_integrity=False
        )
