    def _aggregate_item_by_item(self, func, *args, **kwargs) -> DataFrame:
        # only for axis==0

        obj = self._obj_with_exclusions
        result: Dict[Union[int, str], NDFrame] = {}
        cannot_agg = []
        for item in obj:
            data = obj[item]
            colg = SeriesGroupBy(data, selection=item, grouper=self.grouper)

            cast = self._transform_should_cast(func)
            try:
                result[item] = colg.aggregate(func, *args, **kwargs)

            except ValueError as err:
                if "Must produce aggregated value" in str(err):
                    # raised in _aggregate_named, handle at higher level
                    #  see test_apply_with_mutated_index
                    raise
                # otherwise we get here from an AttributeError in _make_wrapper
                cannot_agg.append(item)
                continue

            else:
                if cast:
                    result[item] = self._try_cast(result[item], data)

        result_columns = obj.columns
        if cannot_agg:
            result_columns = result_columns.drop(cannot_agg)

        return DataFrame(result, columns=result_columns)
