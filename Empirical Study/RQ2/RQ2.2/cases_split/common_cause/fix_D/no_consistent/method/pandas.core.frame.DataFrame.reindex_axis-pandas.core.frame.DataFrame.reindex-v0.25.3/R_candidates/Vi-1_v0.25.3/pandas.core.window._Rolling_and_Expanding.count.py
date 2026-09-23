    def count(self):

        blocks, obj = self._create_blocks()
        # Validate the index
        self._get_index()

        window = self._get_window()
        window = min(window, len(obj)) if not self.center else window

        results = []
        for b in blocks:
            result = b.notna().astype(int)
            result = self._constructor(
                result,
                window=window,
                min_periods=0,
                center=self.center,
                axis=self.axis,
                closed=self.closed,
            ).sum()
            results.append(result)

        return self._wrap_results(results, blocks, obj)
