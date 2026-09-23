    def count(self):

        blocks, obj, index = self._create_blocks(how=None)
        index, indexi = self._get_index(index=index)

        window = self._get_window()
        window = min(window, len(obj)) if not self.center else window

        results = []
        for b in blocks:

            if needs_i8_conversion(b.values):
                result = b.notnull().astype(int)
            else:
                try:
                    result = np.isfinite(b).astype(float)
                except TypeError:
                    result = np.isfinite(b.astype(float)).astype(float)

                result[pd.isnull(result)] = 0

            result = self._constructor(result, window=window, min_periods=0,
                                       center=self.center).sum()
            results.append(result)

        return self._wrap_results(results, blocks, obj)
