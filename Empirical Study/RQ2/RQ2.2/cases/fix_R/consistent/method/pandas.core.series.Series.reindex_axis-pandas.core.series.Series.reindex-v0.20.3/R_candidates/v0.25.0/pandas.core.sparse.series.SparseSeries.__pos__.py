    def __pos__(self):
        result = self.values.__pos__()
        return self._constructor(
            result,
            index=self.index,
            sparse_index=self.sp_index,
            fill_value=result.fill_value,
            copy=False,
        ).__finalize__(self)
