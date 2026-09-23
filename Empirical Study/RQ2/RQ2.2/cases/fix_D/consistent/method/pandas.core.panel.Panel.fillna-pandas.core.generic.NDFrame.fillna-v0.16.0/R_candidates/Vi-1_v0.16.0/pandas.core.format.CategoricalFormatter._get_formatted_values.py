    def _get_formatted_values(self):
        return format_array(self.categorical.get_values(), None,
                            float_format=None,
                            na_rep=self.na_rep)
