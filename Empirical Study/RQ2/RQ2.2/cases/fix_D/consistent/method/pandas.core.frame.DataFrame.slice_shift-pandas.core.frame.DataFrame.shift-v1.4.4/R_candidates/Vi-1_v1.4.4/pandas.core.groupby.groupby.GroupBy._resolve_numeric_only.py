    def _resolve_numeric_only(self, numeric_only: bool | lib.NoDefault) -> bool:
        """
        Determine subclass-specific default value for 'numeric_only'.

        For SeriesGroupBy we want the default to be False (to match Series behavior).
        For DataFrameGroupBy we want it to be True (for backwards-compat).

        Parameters
        ----------
        numeric_only : bool or lib.no_default

        Returns
        -------
        bool
        """
        # GH#41291
        if numeric_only is lib.no_default:
            # i.e. not explicitly passed by user
            if self.obj.ndim == 2:
                # i.e. DataFrameGroupBy
                numeric_only = True
                # GH#42395 GH#43108 GH#43154
                # Regression from 1.2.5 to 1.3 caused object columns to be dropped
                if self.axis:
                    obj = self._obj_with_exclusions.T
                else:
                    obj = self._obj_with_exclusions
                check = obj._get_numeric_data()
                if len(obj.columns) and not len(check.columns) and not obj.empty:
                    numeric_only = False
                    # TODO: v1.4+ Add FutureWarning

            else:
                numeric_only = False

        # error: Incompatible return value type (got "Union[bool, NoDefault]",
        # expected "bool")
        return numeric_only  # type: ignore[return-value]
