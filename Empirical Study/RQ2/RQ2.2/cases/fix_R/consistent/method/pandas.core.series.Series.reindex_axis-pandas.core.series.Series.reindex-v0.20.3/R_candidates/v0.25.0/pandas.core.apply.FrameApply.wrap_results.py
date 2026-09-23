    def wrap_results(self):
        results = self.results

        # see if we can infer the results
        if len(results) > 0 and is_sequence(results[0]):

            return self.wrap_results_for_axis()

        # dict of scalars
        result = self.obj._constructor_sliced(results)
        result.index = self.res_index

        return result
