    def _wrap_result(self, result, block=None, obj=None):
        """
        Wrap a single result.
        """

        if obj is None:
            obj = self._selected_obj
        index = obj.index

        if isinstance(result, np.ndarray):

            if result.ndim == 1:
                from pandas import Series

                return Series(result, index, name=obj.name)

            return type(obj)(result, index=index, columns=block.columns)
        return result
