    @doc(DataFrame.describe)
    def describe(
        self,
        percentiles=None,
        include=None,
        exclude=None,
    ) -> NDFrameT:
        obj = self._obj_with_exclusions

        if len(obj) == 0:
            described = obj.describe(
                percentiles=percentiles, include=include, exclude=exclude
            )
            if obj.ndim == 1:
                result = described
            else:
                result = described.unstack()
            return result.to_frame().T.iloc[:0]

        with com.temp_setattr(self, "as_index", True):
            result = self._python_apply_general(
                lambda x: x.describe(
                    percentiles=percentiles, include=include, exclude=exclude
                ),
                obj,
                not_indexed_same=True,
            )
        if self.axis == 1:
            return result.T

        # GH#49256 - properly handle the grouping column(s)
        result = result.unstack()
        if not self.as_index:
            result = self._insert_inaxis_grouper(result)
            result.index = default_index(len(result))

        return result
