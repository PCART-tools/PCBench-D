    def __getitem__(self, key):
        try:
            return super(Resampler, self).__getitem__(key)
        except (KeyError, com.AbstractMethodError):

            # compat for deprecated
            if isinstance(self.obj, com.ABCSeries):
                return self._deprecated('__getitem__')[key]

            raise
