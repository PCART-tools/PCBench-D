    def strftime(self, date_format):
        return np.asarray(self.format(date_format=date_format),
                          dtype=compat.text_type)
