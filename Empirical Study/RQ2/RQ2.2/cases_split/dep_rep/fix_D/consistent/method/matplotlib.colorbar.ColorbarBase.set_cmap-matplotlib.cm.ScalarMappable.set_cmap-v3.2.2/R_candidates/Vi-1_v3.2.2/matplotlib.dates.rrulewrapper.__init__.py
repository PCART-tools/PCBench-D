    def __init__(self, freq, tzinfo=None, **kwargs):
        kwargs['freq'] = freq
        self._base_tzinfo = tzinfo

        self._update_rrule(**kwargs)
