    def apply_standard(self):
        results, res_index = self.apply_series_generator()

        # wrap results
        return self.wrap_results(results, res_index)
