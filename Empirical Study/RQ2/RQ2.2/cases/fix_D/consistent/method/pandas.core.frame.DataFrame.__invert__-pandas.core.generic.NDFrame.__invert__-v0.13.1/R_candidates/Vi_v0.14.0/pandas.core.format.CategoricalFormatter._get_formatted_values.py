    def _get_formatted_values(self):
        return format_array(np.asarray(self.categorical), None,
                            float_format=None,
                            na_rep=self.na_rep)
