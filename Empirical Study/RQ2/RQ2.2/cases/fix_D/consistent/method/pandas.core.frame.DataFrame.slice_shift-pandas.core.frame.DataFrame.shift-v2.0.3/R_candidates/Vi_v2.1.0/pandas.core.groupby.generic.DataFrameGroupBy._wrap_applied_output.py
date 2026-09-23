    def _wrap_applied_output(
        self,
        data: DataFrame,
        values: list,
        not_indexed_same: bool = False,
        is_transform: bool = False,
    ):
        if len(values) == 0:
            if is_transform:
                # GH#47787 see test_group_on_empty_multiindex
                res_index = data.index
            else:
                res_index = self.grouper.result_index

            result = self.obj._constructor(index=res_index, columns=data.columns)
            result = result.astype(data.dtypes, copy=False)
            return result

        # GH12824
        # using values[0] here breaks test_groupby_apply_none_first
        first_not_none = next(com.not_none(*values), None)

        if first_not_none is None:
            # GH9684 - All values are None, return an empty frame.
            return self.obj._constructor()
        elif isinstance(first_not_none, DataFrame):
            return self._concat_objects(
                values,
                not_indexed_same=not_indexed_same,
                is_transform=is_transform,
            )

        key_index = self.grouper.result_index if self.as_index else None

        if isinstance(first_not_none, (np.ndarray, Index)):
            # GH#1738: values is list of arrays of unequal lengths
            #  fall through to the outer else clause
            # TODO: sure this is right?  we used to do this
            #  after raising AttributeError above
            # GH 18930
            if not is_hashable(self._selection):
                # error: Need type annotation for "name"
                name = tuple(self._selection)  # type: ignore[var-annotated, arg-type]
            else:
                # error: Incompatible types in assignment
                # (expression has type "Hashable", variable
                # has type "Tuple[Any, ...]")
                name = self._selection  # type: ignore[assignment]
            return self.obj._constructor_sliced(values, index=key_index, name=name)
        elif not isinstance(first_not_none, Series):
            # values are not series or array-like but scalars
            # self._selection not passed through to Series as the
            # result should not take the name of original selection
            # of columns
            if self.as_index:
                return self.obj._constructor_sliced(values, index=key_index)
            else:
                result = self.obj._constructor(values, columns=[self._selection])
                result = self._insert_inaxis_grouper(result)
                return result
        else:
            # values are Series
            return self._wrap_applied_output_series(
                values,
                not_indexed_same,
                first_not_none,
                key_index,
                is_transform,
            )
