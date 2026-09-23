    def _set_subtyp(self, is_all_dates):
        if is_all_dates:
            object.__setattr__(self, '_subtyp', 'time_series')
        else:
            object.__setattr__(self, '_subtyp', 'series')
