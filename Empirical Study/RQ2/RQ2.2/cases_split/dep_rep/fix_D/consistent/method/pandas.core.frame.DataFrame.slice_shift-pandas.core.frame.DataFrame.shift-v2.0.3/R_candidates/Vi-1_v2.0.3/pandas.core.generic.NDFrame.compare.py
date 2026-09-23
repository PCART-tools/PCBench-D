    @doc(_shared_docs["compare"], klass=_shared_doc_kwargs["klass"])
    def compare(
        self,
        other,
        align_axis: Axis = 1,
        keep_shape: bool_t = False,
        keep_equal: bool_t = False,
        result_names: Suffixes = ("self", "other"),
    ):
        if type(self) is not type(other):
            cls_self, cls_other = type(self).__name__, type(other).__name__
            raise TypeError(
                f"can only compare '{cls_self}' (not '{cls_other}') with '{cls_self}'"
            )

        mask = ~((self == other) | (self.isna() & other.isna()))
        mask.fillna(True, inplace=True)

        if not keep_equal:
            self = self.where(mask)
            other = other.where(mask)

        if not keep_shape:
            if isinstance(self, ABCDataFrame):
                cmask = mask.any()
                rmask = mask.any(axis=1)
                self = self.loc[rmask, cmask]
                other = other.loc[rmask, cmask]
            else:
                self = self[mask]
                other = other[mask]
        if not isinstance(result_names, tuple):
            raise TypeError(
                f"Passing 'result_names' as a {type(result_names)} is not "
                "supported. Provide 'result_names' as a tuple instead."
            )

        if align_axis in (1, "columns"):  # This is needed for Series
            axis = 1
        else:
            axis = self._get_axis_number(align_axis)

        diff = concat([self, other], axis=axis, keys=result_names)

        if axis >= self.ndim:
            # No need to reorganize data if stacking on new axis
            # This currently applies for stacking two Series on columns
            return diff

        ax = diff._get_axis(axis)
        ax_names = np.array(ax.names)

        # set index names to positions to avoid confusion
        ax.names = np.arange(len(ax_names))

        # bring self-other to inner level
        order = list(range(1, ax.nlevels)) + [0]
        if isinstance(diff, ABCDataFrame):
            diff = diff.reorder_levels(order, axis=axis)
        else:
            diff = diff.reorder_levels(order)

        # restore the index names in order
        diff._get_axis(axis=axis).names = ax_names[order]

        # reorder axis to keep things organized
        indices = (
            np.arange(diff.shape[axis]).reshape([2, diff.shape[axis] // 2]).T.flatten()
        )
        diff = diff.take(indices, axis=axis)

        return diff
