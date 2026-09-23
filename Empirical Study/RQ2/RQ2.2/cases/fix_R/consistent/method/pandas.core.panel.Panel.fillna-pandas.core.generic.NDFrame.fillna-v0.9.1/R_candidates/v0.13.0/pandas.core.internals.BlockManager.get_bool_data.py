    def get_bool_data(self, **kwargs):
        kwargs['is_bool'] = True
        return self.get_data(**kwargs)
