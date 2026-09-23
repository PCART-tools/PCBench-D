    def get_numeric_data(self, **kwargs):
        kwargs['is_numeric'] = True
        return self.get_data(**kwargs)
