    def _resolve_numeric_only(
        self, how: str, numeric_only: bool | lib.NoDefault, axis: int
    ) -> bool:
        """
        Determine subclass-specific default value for 'numeric_only'.

        For SeriesGroupBy we want the default to be False (to match Series behavior).
        For DataFrameGroupBy we want it to be True (for backwards-compat).

        Parameters
        ----------
        numeric_only : bool or lib.no_default
        axis : int
            Axis passed to the groupby op (not self.axis).

        Returns
        -------
        bool
        """
        # GH#41291
        if numeric_only is lib.no_default:
            # i.e. not explicitly passed by user
            if self.obj.ndim == 2:
                # i.e. DataFrameGroupBy
                numeric_only = axis != 1
                # GH#42395 GH#43108 GH#43154
                # Regression from 1.2.5 to 1.3 caused object columns to be dropped
                if self.axis:
                    obj = self._obj_with_exclusions.T
                else:
                    obj = self._obj_with_exclusions
                check = obj._get_numeric_data()
                if len(obj.columns) and not len(check.columns) and not obj.empty:
                    numeric_only = False

            else:
                numeric_only = False

        if numeric_only and self.obj.ndim == 1 and not is_numeric_dtype(self.obj.dtype):
            # GH#47500
            warnings.warn(
                f"{type(self).__name__}.{how} called with "
                f"numeric_only={numeric_only} and dtype {self.obj.dtype}. This will "
                "raise a TypeError in a future version of pandas",
                category=FutureWarning,
                stacklevel=find_stack_level(inspect.currentframe()),
            )
            raise NotImplementedError(
                f"{type(self).__name__}.{how} does not implement numeric_only"
            )

        return numeric_only
