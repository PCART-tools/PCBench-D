    def apply_series_generator(self):
        series_gen = self.series_generator
        res_index = self.result_index

        i = None
        keys = []
        results = {}
        if self.ignore_failures:
            successes = []
            for i, v in enumerate(series_gen):
                try:
                    results[i] = self.f(v)
                    keys.append(v.name)
                    successes.append(i)
                except Exception:
                    pass

            # so will work with MultiIndex
            if len(successes) < len(res_index):
                res_index = res_index.take(successes)

        else:
            try:
                for i, v in enumerate(series_gen):
                    results[i] = self.f(v)
                    keys.append(v.name)
            except Exception as e:
                if hasattr(e, 'args'):

                    # make sure i is defined
                    if i is not None:
                        k = res_index[i]
                        e.args = e.args + ('occurred at index %s' %
                                           pprint_thing(k), )
                raise

        self.results = results
        self.res_index = res_index
        self.res_columns = self.result_columns
