    @cache_readonly
    def _timezone(self):
        """ Comparable timezone both for pytz / dateutil"""
        return libts.get_timezone(self.tzinfo)
