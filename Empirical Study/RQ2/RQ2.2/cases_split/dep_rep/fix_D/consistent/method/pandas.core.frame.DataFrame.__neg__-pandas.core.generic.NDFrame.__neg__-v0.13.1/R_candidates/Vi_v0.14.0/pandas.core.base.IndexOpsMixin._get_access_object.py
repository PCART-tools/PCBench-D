    def _get_access_object(self):
        if isinstance(self, com.ABCSeries):
            return self.index
        return self
