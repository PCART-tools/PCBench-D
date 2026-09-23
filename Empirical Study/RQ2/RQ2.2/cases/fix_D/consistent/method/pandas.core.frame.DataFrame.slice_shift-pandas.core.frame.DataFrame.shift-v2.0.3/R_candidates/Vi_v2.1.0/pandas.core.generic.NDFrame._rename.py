    @final
    def _rename(
        self,
        mapper: Renamer | None = None,
        *,
        index: Renamer | None = None,
        columns: Renamer | None = None,
        axis: Axis | None = None,
        copy: bool_t | None = None,
        inplace: bool_t = False,
        level: Level | None = None,
        errors: str = "ignore",
    ) -> Self | None:
        # called by Series.rename and DataFrame.rename

        if mapper is None and index is None and columns is None:
            raise TypeError("must pass an index to rename")

        if index is not None or columns is not None:
            if axis is not None:
                raise TypeError(
                    "Cannot specify both 'axis' and any of 'index' or 'columns'"
                )
            if mapper is not None:
                raise TypeError(
                    "Cannot specify both 'mapper' and any of 'index' or 'columns'"
                )
        else:
            # use the mapper argument
            if axis and self._get_axis_number(axis) == 1:
                columns = mapper
            else:
                index = mapper

        self._check_inplace_and_allows_duplicate_labels(inplace)
        result = self if inplace else self.copy(deep=copy and not using_copy_on_write())

        for axis_no, replacements in enumerate((index, columns)):
            if replacements is None:
                continue

            ax = self._get_axis(axis_no)
            f = common.get_rename_function(replacements)

            if level is not None:
                level = ax._get_level_number(level)

            # GH 13473
            if not callable(replacements):
                if ax._is_multi and level is not None:
                    indexer = ax.get_level_values(level).get_indexer_for(replacements)
                else:
                    indexer = ax.get_indexer_for(replacements)

                if errors == "raise" and len(indexer[indexer == -1]):
                    missing_labels = [
                        label
                        for index, label in enumerate(replacements)
                        if indexer[index] == -1
                    ]
                    raise KeyError(f"{missing_labels} not found in axis")

            new_index = ax._transform_index(f, level=level)
            result._set_axis_nocheck(new_index, axis=axis_no, inplace=True, copy=False)
            result._clear_item_cache()

        if inplace:
            self._update_inplace(result)
            return None
        else:
            return result.__finalize__(self, method="rename")
