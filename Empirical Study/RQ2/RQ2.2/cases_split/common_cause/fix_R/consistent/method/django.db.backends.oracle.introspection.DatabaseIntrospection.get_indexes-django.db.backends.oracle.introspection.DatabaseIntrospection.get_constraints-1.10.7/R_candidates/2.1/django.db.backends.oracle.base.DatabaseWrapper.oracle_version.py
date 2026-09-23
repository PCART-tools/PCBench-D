    @cached_property
    def oracle_version(self):
        try:
            return int(self.oracle_full_version.split('.')[0])
        except ValueError:
            return None
