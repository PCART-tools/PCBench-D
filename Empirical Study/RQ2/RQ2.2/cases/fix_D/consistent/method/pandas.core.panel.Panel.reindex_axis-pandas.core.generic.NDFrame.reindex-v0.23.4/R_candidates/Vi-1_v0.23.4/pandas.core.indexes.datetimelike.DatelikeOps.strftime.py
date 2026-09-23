    def strftime(self, date_format):
        return Index(self.format(date_format=date_format),
                     dtype=compat.text_type)
