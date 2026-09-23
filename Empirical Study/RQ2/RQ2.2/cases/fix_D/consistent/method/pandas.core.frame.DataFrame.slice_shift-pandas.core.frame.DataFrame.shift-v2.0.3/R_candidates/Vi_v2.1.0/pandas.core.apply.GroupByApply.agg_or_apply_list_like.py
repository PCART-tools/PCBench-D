    def agg_or_apply_list_like(
        self, op_name: Literal["agg", "apply"]
    ) -> DataFrame | Series:
        obj = self.obj
        kwargs = self.kwargs
        if op_name == "apply":
            kwargs = {**kwargs, "by_row": False}

        if getattr(obj, "axis", 0) == 1:
            raise NotImplementedError("axis other than 0 is not supported")

        if obj._selected_obj.ndim == 1:
            # For SeriesGroupBy this matches _obj_with_exclusions
            selected_obj = obj._selected_obj
        else:
            selected_obj = obj._obj_with_exclusions

        # Only set as_index=True on groupby objects, not Window or Resample
        # that inherit from this class.
        with com.temp_setattr(
            obj, "as_index", True, condition=hasattr(obj, "as_index")
        ):
            keys, results = self.compute_list_like(op_name, selected_obj, kwargs)
        result = self.wrap_results_list_like(keys, results)
        return result
