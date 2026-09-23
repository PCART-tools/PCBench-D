    def get_hinting_type(self):
        from matplotlib.backends import backend_agg
        return backend_agg.get_hinting_flag()
