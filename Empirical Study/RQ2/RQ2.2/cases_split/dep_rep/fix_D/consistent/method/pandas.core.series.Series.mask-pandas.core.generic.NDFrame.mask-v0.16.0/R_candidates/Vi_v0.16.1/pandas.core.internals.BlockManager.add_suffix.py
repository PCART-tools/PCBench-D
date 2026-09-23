    def add_suffix(self, suffix):
        f = ('%s' + str(suffix)).__mod__
        return self.rename_axis(f, axis=0)
