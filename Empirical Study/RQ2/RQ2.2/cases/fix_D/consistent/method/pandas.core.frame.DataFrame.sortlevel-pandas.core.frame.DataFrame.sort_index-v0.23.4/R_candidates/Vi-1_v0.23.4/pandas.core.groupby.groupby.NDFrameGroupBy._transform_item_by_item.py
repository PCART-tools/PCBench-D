    def _transform_item_by_item(self, obj, wrapper):
        # iterate through columns
        output = {}
        inds = []
        for i, col in enumerate(obj):
            try:
                output[col] = self[col].transform(wrapper)
                inds.append(i)
            except Exception:
                pass

        if len(output) == 0:  # pragma: no cover
            raise TypeError('Transform function invalid for data types')

        columns = obj.columns
        if len(output) < len(obj.columns):
            columns = columns.take(inds)

        return DataFrame(output, index=obj.index, columns=columns)
