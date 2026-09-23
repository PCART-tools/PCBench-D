    def _transform_item_by_item(self, obj: DataFrame, wrapper) -> DataFrame:
        # iterate through columns, see test_transform_exclude_nuisance
        #  gets here with non-unique columns
        output = {}
        inds = []
        for i, (colname, sgb) in enumerate(self._iterate_column_groupbys(obj)):
            try:
                output[i] = sgb.transform(wrapper)
            except TypeError:
                # e.g. trying to call nanmean with string values
                warn_dropping_nuisance_columns_deprecated(type(self), "transform")
            else:
                inds.append(i)

        if not output:
            raise TypeError("Transform function invalid for data types")

        columns = obj.columns.take(inds)

        result = self.obj._constructor(output, index=obj.index)
        result.columns = columns
        return result
