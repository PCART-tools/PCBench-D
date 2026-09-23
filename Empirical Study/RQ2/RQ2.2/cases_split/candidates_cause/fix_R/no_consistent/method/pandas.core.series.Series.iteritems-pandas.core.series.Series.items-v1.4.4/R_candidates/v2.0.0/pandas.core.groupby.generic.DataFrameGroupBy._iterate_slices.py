    def _iterate_slices(self) -> Iterable[Series]:
        obj = self._selected_obj
        if self.axis == 1:
            obj = obj.T

        if isinstance(obj, Series) and obj.name not in self.exclusions:
            # Occurs when doing DataFrameGroupBy(...)["X"]
            yield obj
        else:
            for label, values in obj.items():
                if label in self.exclusions:
                    # Note: if we tried to just iterate over _obj_with_exclusions,
                    #  we would break test_wrap_agg_out by yielding a column
                    #  that is skipped here but not dropped from obj_with_exclusions
                    continue

                yield values
