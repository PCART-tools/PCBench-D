    def apply_series_generator(self) -> Tuple[ResType, "Index"]:
        series_gen = self.series_generator
        res_index = self.result_index

        keys = []
        results = {}
        if self.ignore_failures:
            successes = []
            for i, v in enumerate(series_gen):
                try:
                    results[i] = self.f(v)
                except Exception:
                    pass
                else:
                    keys.append(v.name)
                    successes.append(i)

            # so will work with MultiIndex
            if len(successes) < len(res_index):
                res_index = res_index.take(successes)

        else:
            for i, v in enumerate(series_gen):
                results[i] = self.f(v)
                keys.append(v.name)

        return results, res_index
