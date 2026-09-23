    def _aggregate_item_by_item(self, func, *args, **kwargs):
        # only for axis==0

        obj = self._obj_with_exclusions
        result = OrderedDict()
        cannot_agg = []
        errors = None
        for item in obj:
            try:
                data = obj[item]
                colg = SeriesGroupBy(data, selection=item, grouper=self.grouper)

                cast = self._transform_should_cast(func)

                result[item] = colg.aggregate(func, *args, **kwargs)
                if cast:
                    result[item] = self._try_cast(result[item], data)

            except ValueError:
                cannot_agg.append(item)
                continue
            except TypeError as e:
                cannot_agg.append(item)
                errors = e
                continue

        result_columns = obj.columns
        if cannot_agg:
            result_columns = result_columns.drop(cannot_agg)

            # GH6337
            if not len(result_columns) and errors is not None:
                raise errors

        return DataFrame(result, columns=result_columns)
