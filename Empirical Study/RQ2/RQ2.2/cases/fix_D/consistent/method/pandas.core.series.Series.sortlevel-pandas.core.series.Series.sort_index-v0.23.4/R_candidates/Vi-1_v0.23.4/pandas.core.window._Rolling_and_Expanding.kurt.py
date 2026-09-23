    def kurt(self, **kwargs):
        return self._apply('roll_kurt', 'kurt',
                           check_minp=_require_min_periods(4), **kwargs)
