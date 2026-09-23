    def _get_formatted_values(self):
        return format_array(self.series.get_values(), None,
                            float_format=self.float_format,
                            na_rep=self.na_rep)
