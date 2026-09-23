    def count(self):

        blocks, obj = self._create_blocks()
        results = []
        for b in blocks:
            result = b.notna().astype(int)
            result = self._constructor(
                result,
                window=self._get_window(),
                min_periods=self.min_periods or 0,
                center=self.center,
                axis=self.axis,
                closed=self.closed,
            ).sum()
            results.append(result)

        return self._wrap_results(results, blocks, obj)
